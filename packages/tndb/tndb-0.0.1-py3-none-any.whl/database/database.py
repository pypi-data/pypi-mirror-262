"""数据库公共类(主类)
参数标准为PostgreSQL

Returns:
    _type_: _description_
"""
import os
import re
import json
import asyncio
import pymysql
import aiomysql
import psycopg2
import asyncpg
import warnings


def kwargs_check(kwargs: dict):
    """检查参数
    将mysql的参数键与pgsql的参数键进行统一,并且设置默认值

    Args:
        kwargs (_type_): _description_
    """
    # 设置新的对象
    obj = {}
    # 服务器地址
    obj["host"] = kwargs.get("host", "localhost")
    # 自动提交
    obj["autocommit"] = kwargs.get("autocommit", True)
    # 判断是否使用连接池
    obj["pool"] = kwargs.get("pool", False)
    # 如果使用连接池,赋值事件循环
    if obj["pool"]:
        obj["loop"] = kwargs.get("loop", asyncio.get_event_loop())

    # 自动判断数据库类型,目前仅支持mysql.pgsql
    if "database" in kwargs:
        # pgsql数据库
        obj["genre"] = "pgsql"
        # 用户名
        obj["user"] = kwargs.get("user", "postgres")
        # 密码
        obj["password"] = kwargs.get("password", "postgres")
        # 端口
        obj["port"] = kwargs.get("port", 5432)
        # 最小连接池
        obj["min_size"] = kwargs.get("min_size", 1)
        # 最大连接池
        obj["max_size"] = kwargs.get("max_size", 10)
        # 数据库名
        obj["database"] = kwargs.get("database", "postgres")
        # 架构
        obj["schema"] = kwargs.get("schema", kwargs["database"])
        # 最大查询次数
        obj["max_queries"] = kwargs.get("max_queries", 5000)
        # 最大连接时间
        obj["max_inactive_connection_lifetime"] = kwargs.get(
            "max_inactive_connection_lifetime", 300)
        # 调试开关
        obj["debug"] = kwargs.get("debug", False)

    else:
        # mysql数据库
        obj["genre"] = "mysql"
        # 用户名
        obj["user"] = kwargs.get("user", "root")
        # 密码
        obj["password"] = kwargs.get("password", "root")
        # 端口
        obj["port"] = kwargs.get("port", 3306)
        # 最小连接池
        obj["minsize"] = kwargs.pop("min_size", 1)
        # 最大连接池
        obj["maxsize"] = kwargs.pop("max_size", 10)
        # 数据库名
        obj["db"] = kwargs.pop("schema", "mysql")
        # 数据库字符
        obj["charset"] = kwargs.get("charset", "utf8mb4")
        # 连接超时
        obj["connect_timeout"] = kwargs.get("connect_timeout", 10)
        # 打印语句
        obj["echo"] = kwargs.get("echo", False)
        # 调试开关
        obj["debug"] = kwargs.get("debug", False)
        # 游标返回类型 aiomysql.cursors.DictCursor 或 pymysql.cursors.DictCursor|这是返回json  目前还没想好怎么把这个对象拿进来
        obj["cursorclass"] = kwargs.get("cursorclass", None)
        # 加密协议 入字典{"cert":"/path/cert.pem","key":"/path/key.pem"}
        obj["ssl"] = kwargs.get("ssl", {})
        # 服务器公钥
        obj["server_public_key"] = kwargs.get("server_public_key", "")
    return obj


def replace_text(text, pattern, repl, count=1, case_sensitive=False) -> str:
    """替换文本

    Args:
        text (_type_): 源文本
        pattern (_type_): 被替换的文本
        repl (_type_): 用作替换的文本
        count (int, optional): 替换次数. Defaults to 1.
        case_sensitive (bool, optional): 不区分大小写. Defaults to False.

    Returns:
        _type_: 替换后的文本
    """
    # 正则匹配字符串
    if case_sensitive:
        return re.sub(pattern, repl, text, count=count)
    else:
        return re.sub(pattern, repl, text, count=count, flags=re.IGNORECASE)


def table_name_process(table_name, schema, self_schema) -> str:
    """表名处理

    Args:
        table_name (_type_): 表名
        schema (_type_): 函数类表名,该参数优先级最高,如果不为空,则不会考虑self_schema
        self_schema (_type_): 类表名

    Returns:
        str: 返回处理后的表名
    """
    if schema:
        return f"{schema}.{table_name}"
    elif self_schema:
        return f"{self_schema}.{table_name}"
    else:
        return table_name


def condition_process(condition: str) -> str:
    """条件处理

    Args:
        condition (_type_): 条件

    Returns:
        _type_: 返回处理后的条件
    """
    if not condition:
        condition = ""
        return ""

    # 去除左边空字符
    condition.lstrip()
    # 判断开头是否为AND
    if condition.upper().startswith("AND"):
        # 将AND替换成功WHERE
        condition = condition.replace(
            "AND", "WHERE", 1)
        return f" {condition} "

    # 如果开头不为AND,判断是否为OR
    if condition.upper().startswith("OR"):
        # 将OR替换为WHERE
        condition = condition.replace(
            "OR", "WHERE", 1)
        return f" {condition} "

    # 如果没有AND和OR,就在条件前面加上WHERE
    condition = f" WHERE {condition} "
    return condition

def filter_process(genre:str="pgsql",sql: str="",group:str=None,order:str=None,limit:str=None) -> str:
    """过滤处理,默认为pgsql

    Args:
        genre (str, optional): _description_. Defaults to "pgsql".
        sql (str, optional): _description_. Defaults to "".
        group (str, optional): _description_. Defaults to None.
        order (str, optional): _description_. Defaults to None.
        limit (str, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    if group:
        sql += f" GROUP BY {group}"
    if order:
        sql += f" ORDER BY {order}"
    if limit:
        if genre == "mysql":
            if isinstance(limit, int):
                limit = str(limit)
            else:
                limit.lstrip().rstrip()
            if " " in limit and "," not in limit:
                limit.replace(" ", ",")
        else:
            if isinstance(limit, str) and "OFFSET" not in limit.upper() and "," in limit:
                limit.replace(",", " OFFSET ")
        sql += f" LIMIT {limit}"    
    return sql

class Database:
    def __init__(self, **kwargs):
        """初始化
        """
        # 赋值参数
        self.kwargs = kwargs_check(kwargs)
        # 设置参数默认值
        self.conn = None
        self.debug = self.kwargs.pop("debug")
        self.genre = self.kwargs.pop("genre")
        self.pool = self.kwargs.pop("pool")
        self.schema = self.kwargs.get("db", self.kwargs.get("scheam", ""))
        if self.pool:
            self.transaction = None
            self.lock = asyncio.Lock()

            # 解释一下下面的代码
            """当外部启动为同步启动时,会在这里启动异步,例子如下:
            主方法():#这是同步启动方法---外部
                db=Database()

            __init__()#这是Database()执行后的初始化函数
                self.loop = self.kwargs.pop("loop") #这个函数是拿当前环境的事件循环
                    if not self.loop.is_running():#拿到之后来看一下这个事件循环是否在运行,如果没有运行,代表是同步启动
                        self.loop.run_until_complete(self.connect_async())#因为是同步启动,没有事件循环在运行,所以这里需要开启一个事件循环

            下面这个例子为异步启动:
            async 主方法():这是异步启动方法,外部
                db=Database()#实例化
                await db.connect() #因为是在异步里启动的,所以启动里面不会再启动事件,既然启动里没有启动事件循环了,这里就需要直接调用连接,因为这里本身就处于事件循环里面,所以不需要再启动事件循环,在启动方法里就已经启动了,这里直接进行连接就可以了
            
            启动方法():
                asyncio.run(主方法())
            
            __init__()#这是Database()执行后的初始化函数
                self.loop = self.kwargs.pop("loop") #这个函数是拿当前环境的事件循环
                    if not self.loop.is_running():#拿到之后来看一下这个事件循环是否在运行,如果在运行,则不管,因为在外部需要来运行事件循环
                        self.loop.run_until_complete(self.connect_async())#因为是同步启动,没有事件循环在运行,所以这里需要开启一个事件循环
            """
            self.loop = self.kwargs.pop("loop")
            if not self.loop.is_running():
                self.loop.run_until_complete(self.connect_async())

        else:
            # 不使用连接池
            # 去掉一些参数
            self.kwargs.pop("minsize")
            self.kwargs.pop("maxsize")
            self.kwargs.pop("echo")
            self.connect()

# ====同步====
    def connect(self) -> None:
        """连接数据库_同步

        Returns:
            _type_: _description_
        """
        try:
            self.conn = pymysql.connect(
                **self.kwargs) if self.genre == "mysql" else psycopg2.connect(**self.kwargs)

            print(f"{self.genre}数据库连接成功")
        except Exception as e:
            print(f"{self.genre}数据库连接失败:{str(e)}")
            os._exit(0)

    def close(self) -> None:
        """关闭_同步
        """
        # 结束事务
        self.transaction_end()
        # 关闭连接
        self.conn.close()
        print(f"{self.genre}数据库连接已关闭")

    def transaction_begin(self) -> None:
        """开始事务_同步
        """
        if self.genre == "mysql":  # mysql处理
            # 查看自动提交是否为假,如果是,说明有未结束的事务,先结束它
            self.transaction_end()
            # 将自动提交设置成假,代表开启事务
            self.conn.autocommit(False)
            return

        # pgsql处理
        # 查看自动提交是否为假,如果是,说明有未结束的事务,先结束它
        self.transaction_end()
        # 将自动提交设置成假,代表开启事务
        self.conn.autocommit = False

    def transaction_end(self, success=False) -> None:
        """结束事务_同步

        Args:
            success (bool, optional): 是否成功. Defaults to True.
        """

        if self.genre == "mysql":  # mysql处理
            # 判断是否存在事务,自动提交为真,代表不存在事务
            if self.conn.autocommit_mode:
                return
            if success:
                # 提交事务
                self.conn.commit()
            else:
                # 回滚事务
                self.conn.rollback()
            self.conn.autocommit(True)

        else:  # pgsql处理
            # 判断是否存在事务,自动提交为真,代表不存在事务
            if self.conn.autocommit:
                return
            if success:
                # 提交事务
                self.conn.commit()
            else:
                # 回滚事务
                self.conn.rollback()
            self.conn.autocommit = True

    def execute(self, sql: str, result: dict = {}) -> bool:
        """执行_同步

        Args:
            sql (str): 语句
            result (dict, optional): 返回对象. Defaults to {}.

        Returns:
            bool: 成功返回True,失败返回False
        """

        # 清空返回对象,因为参数为引用对象,直接赋值给另一个变量不会影响到外部对象
        result.clear()

        if self.debug:  # 是否为调试
            result["sql"] = sql

        # 判断是否开启了连接池
        if self.pool:
            if self.debug:  # 是否为调试
                result["error"] = "异步连接不能使用同步方法"
            return False

        if self.genre == "mysql":  # mysql处理
            need_total = "LIMIT" in sql.upper()

        else:  # pgsql处理
            # 判断是否需要总数
            need_total = "LIMIT" in sql.upper() and "OFFSET" in sql.upper()

        if need_total:
            # 查询总数
            # 未查询到数量
            if not self.total(sql=sql, result=result) or result["data"][0]["total"] == 0:
                # 回滚
                self.transaction_end()
                # 直接返回
                return False

            # 查询到数量并赋值数量
            result["total"] = result["data"][0]["total"]
            # 因为查询过了数量,防止sql被更改,所以这里重新赋值
            if self.debug:  # 是否为调试
                result["sql"] = sql

        # 取一个游标
        cursor = self.conn.cursor(
            cursor=pymysql.cursors.DictCursor) if self.genre == "mysql" else self.conn.cursor()
        try:
            if self.genre == "mysql":  # mysql处理
                # 执行语句
                cursor.execute(sql)
            else:  # pgsql处理
                # 执行语句
                data = cursor.execute(sql)
        except Exception as e:
            # 执行失败,赋值错误信息
            if self.debug:  # 是否为调试
                result["error"] = str(e)

        finally:  # 不管成功失败都会走这里
            # 关闭游标
            cursor.close()
            # 初始化data
            data = []
            if self.genre == "mysql":  # mysql处理
                # 拿到数据
                if ("SELECT" in sql.upper()):  # 查询
                    data = cursor.fetchall()
                elif ("TRUNCATE" in sql.upper()):  # 清空
                    return True
                else:  # 执行
                    if cursor.rowcount > 0:
                        # 判断是否为插入,如果是就赋值ID,如果不是就把执行数量赋值total
                        if sql.lstrip().upper().startswith("INSERT"):
                            # 插入返回成功后的ID
                            data = [{"id": cursor.lastrowid}]
                        else:
                            # 其它执行方法,返回total
                            data = [{"total": cursor.rowcount}]

            if len(data) > 0:
                result["data"] = data
                # field = []
                # field = [i[0] for i in cursor.description]
                # data = [dict(zip(field, i)) for i in data]
                # result["data"] = data
                # return True, data
                # 有数据
                return True
            # 防止在查询总数后,没查到数据,会把total返回出去
            if need_total:
                result.pop("data")
                result.pop("total")
            # 回滚
            self.transaction_end()
            return False

    def total(self, sql: str, result: dict = {}) -> bool:
        """查询总数_同步

        Args:
            sql (str): 语句
        """
        # 清空返回对象,因为参数为引用对象,直接赋值给另一个变量不会影响到外部对象
        result.clear()

        if self.debug:  # 是否为调试
            result["sql"] = sql

        # 处理查询语句
        sql = replace_text(sql, r"(?<=SELECT).*?(?=FROM)", " COUNT(1) total ")
        sql = replace_text(sql, r"GROUP BY([\s]+)([\S]+)([\w]+)", "")
        sql = replace_text(sql, r"ORDER BY([\s]+)([\S]+)([\w]+)", "")
        # sql = replace_text(sql, r"LIMIT([\s]+)([\d]+),([\d]+)", "") if self.genre == "mysql" else self.__replace_text(
        #     sql, r"LIMIT([\s]+)([\S]+)([\]+)([\s]+)([\w]+)([\s]+)([\d]+)", "")
        sql = replace_text(sql, r"LIMIT([\s]+)([\d]+)(,*)([\s]*)([\d]*)", "") if self.genre == "mysql" else self.__replace_text(
            sql, r"LIMIT([\s]+)([\S]+)([\]+)([\s]+)([\w]+)([\s]+)([\d]+)", "")
        sql = sql.lstrip().rstrip()
        # 执行并返回
        return self.execute(sql=sql, result=result)

    def insert(self, table: str, key: str = None, value: str = None, json_data: dict = None, schema=None, index: str = None, result: dict = {}) -> bool:
        """插入_同步
        Args:
            table (str): 表名
            key (str, optional): 原字段,语句怎么填的,它就怎么填,不需要带括号. Defaults to None.
            value (str, optional): 原参数,语句怎么填的,他就怎么填,需要带括号. Defaults to None.
            json (dict, optional): json数据,这个参数不为空时,key和value将失效,json的键必须在数据库有对应的字段,否则失败,可以在传入前在外面处理好. Defaults to None.
            schema (_type_, optional): 在mysql中这个参数代表数据库,在pgsql中代表架构. Defaults to None.
            index (str, optional): 返回索引ID,仅在pgsql中生效. Defaults to None.
            result (dict, optional): 返回对象,包含了数据/错误信息/语句等. Defaults to {}.

        Returns:
            bool: 成功|true 失败|false
        """
        # 对象参数是否存在
        if json_data:
            # 将键值初始化为空
            key = value = ""
            # 临时列表,用来存取出来的值,方便后面一次性组装
            tem_list = []

            if isinstance(json_data, list):  # 对象为列表时
                # 参数为列表,先取出所有的键
                key = ",".join(json_data[0].keys())
                # 循环取出每一组的对象
                for item in json_data:
                    # 将取出的对象值进行判断是否为对象或列表,如果是,将其转成文本,并加入临时列表
                    tem_list.append(
                        "("+",".join(f"'{json.dumps(i,ensure_ascii=False) if isinstance(i, dict) or isinstance(i, list) else str(i)}'" for i in item.values())+")")
                value = ",".join(tem_list)

                if self.genre == "mysql":
                    # 如果时mysql,将None替换成空字符
                    value = value.replace("'None'", "''")
                else:
                    # 如果是pgsql,将None和空字符替换成默认
                    value = valuse.replace("'None'", "DEFAULT")
                    value = value.replace("''", "DEFAULT")
                # 去掉值中第一个逗号
                value = {value[1:]}

            elif isinstance(json_data, dict):  # 对象为字典时
                # 取出该字典的每一项键值
                for k, v in json_data.items():
                    # 将键加入临时列表
                    tem_list.append(k)
                    # 拼接参数
                    if isinstance(v, dict) or isinstance(v, list):
                        # 值为列表或字典时,将其转成文本,并加入临时列表
                        value += f",'{json.dumps(v,ensure_ascii=False)}'"
                    else:
                        if v:
                            # 如果v不为空字符,加入临时列表
                            value += f",'{v}'"
                        else:
                            # 如果是mysql,设置为空字符,如果是pgsql设置为默认
                            value += ",''" if self.genre == "mysql" else ",DEFAULT"
                # 去掉值中第一个逗号
                value = f"({value[1:]})"
            # 取出键
            key = ",".join(tem_list)

        # 处理表名
        table_name = table_name_process(table, schema, self.schema)

        # 拼接语句
        if self.genre == "mysql":
            sql = f"INSERT IGNORE INTO {table_name} ({key}) VALUES {value}"
        else:
            sql = f"INSERT INTO {table_name} ({key}) VALUES {value} ON CONFLICT DO NOTHING" + \
                f" RETURNING {index}" if index else ""

        return self.execute(sql=sql,  result=result)

    def delete(self, table: str, condition: str = None, schema: str = None, result: dict = {}) -> bool:
        """删除_同步

        Args:
            table (str): 表名
            condition (str): 条件,不填则会清空表
            schema (str, optional): 在mysql中这个参数代表数据库,在pgsql中代表架构. Defaults to None.
            result (dict, optional): 返回对象,包含了数据/错误信息/语句等. Defaults to {}.

        Returns:
            bool: 成功|true 失败|false
        """
        # 如果没有条件,则直接清空
        if not condition:
            return self.truncate(table=table, schema=schema, result=result)

        # 处理条件
        condition = condition_process(condition)

        # 处理表名
        table_name = table_name_process(table, schema, self.schema)
        # 拼接语句
        sql = f"DELETE FROM {table_name}{condition}"
        return self.execute(sql=sql,  result=result)

    def update(self, table: str, condition: str = None, kv: str = None, json_data: dict = None, schema: str = None, index: str = None, result: dict = {}) -> bool:
        """更新_同步

        Args:
            table (str): 表名
            condition (str, optional):条件. Defaults to None.
            kv (str, optional): 原参数 a=b,c=d. Defaults to None.
            json_data (dict, optional): 对象参数,如果该参数不为空,kv将失效. Defaults to None.
            schema (str, optional): mysql中为库名,pgsql中为架构. Defaults to None.
            index (str, optional): 仅在pgsql下有效,返回ID. Defaults to None.
            result (dict, optional): 返回对象. Defaults to {}.

        Returns:
            bool: 成功|true 失败|false
        """
        # 对象参数是否存在
        if json_data:
            # 将键值对初始化为空
            kv = ""
            for k, v in json_data.items():
                # 拼接参数
                kv = f"{kv},{k}='{v}'"
            kv = kv[1:]

        # 处理条件
        condition = condition_process(condition)
        # 处理表名
        table_name = table_name_process(table, schema, self.schema)
        # 拼接语句
        sql = f"UPDATE {table_name} SET {kv}{condition}"
        if self.genre == "pgsql":
            sql += f" ON CONFLICT DO NOTHING" + \
                f" RETURNING {index}" if index else ""
        return self.execute(sql=sql, result=result)

    def select(self, table: str, condition: str = None, json_data: dict = None, field: str = "*", limit: str = None, order: str = None, group: str = None, schema: str = None, result: dict = {}) -> bool:
        """查询_同步

        Args:
            table (str): 表名
            condition (str, optional): 条件,json_data不为空时,格式为这样 user_id=`user_id` AND create_time>=`create_time`. Defaults to None.
            json_data (dict, optional): 对象参数. Defaults to None.
            field (str, optional): 字段. Defaults to "*".
            limit (str, optional): 条数. Defaults to None.
            order (str, optional): 排序. Defaults to None.
            group (str, optional): 分组. Defaults to None.
            schema (str, optional): 架构. Defaults to None.
            result (dict, optional): 返回. Defaults to {}.

        Returns:
            bool: _description_
        """
        # 处理条件
        condition = condition_process(condition)
        # 处理表名
        table_name = table_name_process(table, schema, self.schema)
        #处理过滤
        sql=  filter_process(genre=self.genre,sql=f"SELECT {field} FROM {table_name}{condition}",group=group,order=order,limit=limit)
        
        # 如果对象数据不为空,那么就自动替换条件里的参数
        if json_data:
            for key, value in json_data.items():
                sql = sql.replace(f"`{key}`", f"'{value}'")

        return self.execute(sql=sql,  result=result)

    def truncate(self, table: str, schema: str = None, result: dict = {}) -> bool:
        """清空_同步

        Args:
            table (str): 表名
            schema (str, optional): 架构. Defaults to None.

        Returns:
            bool: _description_
        """
        # 处理表名
        table_name = table_name_process(table, schema, self.schema)
        return self.execute(sql=f"TRUNCATE TABLE {table_name}", result=result)

# ====异步====

    async def connect_async(self) -> None:
        """连接数据库_异步

        Returns:
            _type_: _description_
        """
        try:
            self.pool = await aiomysql.create_pool(**self.kwargs) if self.genre == "mysql" else await asyncpg.create_pool(**self.kwargs)
            print(f"{self.genre}连接成功")
        except Exception as e:
            print(f"{self.genre}连接失败:{str(e)}")
            os._exit(0)

    async def close_async(self) -> None:
        """关闭_异步
        """
        # 关闭事务
        await self.transaction_end_async()
        # 关闭连接池
        self.pool.close()
        # 关闭事件循环
        self.loop.stop()

    async def transaction_begin_async(self) -> None:
        """开始事务_异步
        """
        # 开始之前先结束事务
        await self.transaction_end_async()
        # 获取一个连接
        self.conn = await self.pool.acquire()
        # 判断连接类型
        if self.genre == "mysql":  # mysql处理
            # 开启事务
            await self.conn.begin()
        else:  # pgsql处理
            # 获取一个事务
            self.transaction = self.conn.transaction()
            # 开启事务
            await self.transaction.start()

    async def transaction_end_async(self, success=True) -> None:
        """结束事务_异步

        Args:
            success (bool, optional): 是否成功. Defaults to True.
        """
        # 判断连接类型
        if self.genre == "mysql":
            # 判断事务是否存在
            if self.conn:
                # 判断执行是否成功
                if success:
                    # 提交事务
                    await self.conn.commit()
                else:
                    # 回滚事务
                    await self.conn.rollback()
                # 关闭连接
                self.conn.close()
                self.conn = None
        else:  # pgsql处理
            # 判断事务是否存在
            if self.conn:
                # 判断执行是否成功
                if success:
                    # 提交事务
                    await self.transaction.commit()
                else:
                    # 回滚事务
                    await self.transaction.rollback()
                # 关闭连接
                await self.conn.close()
                self.conn = None
                self.transaction = None

    async def execute_async(self, sql: str, result: dict = {}) -> bool:
        """执行_异步

        Args:
            sql (str): 语句
            result (dict, optional): 返回对象. Defaults to {}.

        Returns:
            bool: 成功返回True,失败返回False
        """

        # 清空返回对象,因为参数为引用对象,直接赋值给另一个变量不会影响到外部对象
        result.clear()

        if self.debug:  # 是否为调试
            result["sql"] = sql

        #判断是否开启了连接池
        if not self.pool:
            if self.debug:  # 是否为调试
                result["error"] = "同步连接不能使用异步方法"
            return False

        if self.genre == "mysql":  # mysql处理
            need_total = "LIMIT" in sql.upper()

        else:  # pgsql处理
            # 判断是否需要总数
            need_total = "LIMIT" in sql.upper() and "OFFSET" in sql.upper()

        if need_total:
            # 查询总数
            # 未查询到数量
            if not await self.total_async(sql=sql, result=result) or result["data"][0]["total"] == 0:
                # 回滚
                await self.transaction_end_async()
                # 直接返回
                return False

            # 查询到数量并赋值数量
            result["total"] = result["data"][0]["total"]
            # 因为查询过了数量,防止sql被更改,所以这里重新赋值
            if self.debug:  # 是否为调试
                result["sql"] = sql

        # 判断conn是否为空,从而判断是否有事务,如果没有事务,就从连接池获取一个连接,如果有事务,就将事务连接赋值给变量
        conn = self.conn if self.conn else await self.pool.acquire()

        # 判断连接类型
        if self.genre == "mysql":  # mysql处理
            # 判断是否为查询语句,执行走execute 查询走fatchall

            # 获取一个游标
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # 获取一个锁
                async with self.lock:
                    try:  # 异常块
                        # 执行语句
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            await cursor.execute(sql)
                    except Exception as e:  # 异常处理
                        if self.debug:  # 是否为调试
                            result["error"] = str(e)

                    finally:  # 最终
                        if ("TRUNCATE" in sql.upper()):  # 清空,因为不会有数量返回,所以放在了数量判断的前面
                            if not self.conn:
                                # 没有事务,关闭连接
                                conn.close()
                            return True

                        if cursor.rowcount == 0:  # 未获取到数据
                            # 回滚
                            await self.transaction_end_async()
                            if not self.conn:
                                # 没有事务,关闭连接
                                conn.close()
                            return False
                        # 拿到数据
                        if ("SELECT" in sql.upper()):  # 查询
                            data = await cursor.fetchall()
                        elif ("UPDATE" in sql.upper() or "DELETE" in sql.upper()):  # 更新或删除
                            data = [{"total": cursor.rowcount}]
                        else:  # 执行
                            data = [{"total": cursor.lastrowid}]
                        result["data"] = data
                        if not self.conn:
                            # 没有事务,关闭连接
                            conn.close()
                        return True
        else:  # pgsql处理
            # 判断是否为查询语句,或者是否需要返回ID,如果是则走fetch,否则走execute
            if ("SELECT" in sql.upper() or "RETURNING" in sql.upper()):
                # 获取一个锁
                async with self.lock:
                    try:  # 异常块
                        # 执行查询
                        data = await conn.fetch(sql)

                    except Exception as e:  # 异常处理
                        if self.debug:  # 是否为调试
                            result["error"] = str(e)

                    finally:  # 最终
                        if len(data) < 1:  # 未获取到数据
                            # 回滚
                            await self.transaction_end_async()
                            if not self.conn:
                                # 没有事务,关闭连接
                                conn.close()
                            return False
                        # 拿到数据
                        result["data"] = data
                        if not self.conn:
                            # 没有事务,关闭连接
                            conn.close()
                        return True

            # 不带索引的执行语句
            async with self.lock:  # 获取一个锁
                try:  # 异常块
                    # 执行语句
                    data = await conn.execute(sql)
                except Exception as e:  # 异常处理
                    if self.debug:  # 是否为调试
                        result["error"] = str(e)
                finally:  # 最终

                    # 解析数据
                    arr = data.split(" ")
                    if arr[0] == 'SELECT':
                        total = int(arr[1])
                    elif arr[0] == 'INSERT':
                        total = int(arr[2])
                    else:
                        total = arr

                    if total == 0:  # 数据据
                        # 回滚
                        await self.translation_end()
                        if not self.conn:
                            # 没有事务,关闭连接
                            conn.close()
                        return False

                    # 拿到数据
                    data = [{"total": total}]
                    result["data"] = data
                    if not self.conn:
                        # 没有事务,关闭连接
                        conn.close()
                    return True

    async def total_async(self, sql: str, result: dict = {}) -> bool:
        """查询总数_同步

        Args:
            sql (str): 语句
        """
        # 清空返回对象,因为参数为引用对象,直接赋值给另一个变量不会影响到外部对象
        result.clear()

        if self.debug:  # 是否为调试
            result["sql"] = sql

        # 处理查询语句
        sql = replace_text(sql, r"(?<=SELECT).*?(?=FROM)", " COUNT(1) total ")
        sql = replace_text(sql, r"GROUP BY([\s]+)([\S]+)([\w]+)", "")
        sql = replace_text(sql, r"ORDER BY([\s]+)([\S]+)([\w]+)", "")
        sql = replace_text(sql,r"LIMIT([\s]+)([\d]+)(,*)([\s]*)([\d]*)", "") if self.genre == "mysql" else self.__replace_text(
            sql, r"LIMIT([\s]+)([\S]+)([\]+)([\s]+)([\w]+)([\s]+)([\d]+)", "")

        sql = sql.lstrip().rstrip()
        # 执行并返回
        return await self.execute_async(sql=sql, result=result)

    async def insert_async(self, table: str, key: str = None, value: str = None, json_data: dict = None, schema=None, index: str = None, result: dict = {}) -> bool:
        """插入_同步
        Args:
            table (str): 表名
            key (str, optional): 原字段,语句怎么填的,它就怎么填,不需要带括号. Defaults to None.
            value (str, optional): 原参数,语句怎么填的,他就怎么填,需要带括号. Defaults to None.
            json (dict, optional): json数据,这个参数不为空时,key和value将失效,json的键必须在数据库有对应的字段,否则失败,可以在传入前在外面处理好. Defaults to None.
            schema (_type_, optional): 在mysql中这个参数代表数据库,在pgsql中代表架构. Defaults to None.
            index (str, optional): 返回索引ID,仅在pgsql中生效. Defaults to None.
            result (dict, optional): 返回对象,包含了数据/错误信息/语句等. Defaults to {}.

        Returns:
            bool: 成功|true 失败|false
        """
        # 对象参数是否存在
        if json_data:
            # 将键值初始化为空
            key = value = ""
            # 临时列表,用来存取出来的值,方便后面一次性组装
            tem_list = []

            if isinstance(json_data, list):  # 对象为列表时
                # 参数为列表,先取出所有的键
                key = ",".join(json_data[0].keys())
                # 循环取出每一组的对象
                for item in json_data:
                    # 将取出的对象值进行判断是否为对象或列表,如果是,将其转成文本,并加入临时列表
                    tem_list.append(
                        "("+",".join(f"'{json.dumps(i,ensure_ascii=False) if isinstance(i, dict) or isinstance(i, list) else str(i)}'" for i in item.values())+")")
                value = ",".join(tem_list)

                if self.genre == "mysql":
                    # 如果时mysql,将None替换成空字符
                    value = value.replace("'None'", "''")
                else:
                    # 如果是pgsql,将None和空字符替换成默认
                    value = valuse.replace("'None'", "DEFAULT")
                    value = value.replace("''", "DEFAULT")
                # 去掉值中第一个逗号
                value = {value[1:]}

            elif isinstance(json_data, dict):  # 对象为字典时
                # 取出该字典的每一项键值
                for k, v in json_data.items():
                    # 将键加入临时列表
                    tem_list.append(k)
                    # 拼接参数
                    if isinstance(v, dict) or isinstance(v, list):
                        # 值为列表或字典时,将其转成文本,并加入临时列表
                        value += f",'{json.dumps(v,ensure_ascii=False)}'"
                    else:
                        if v:
                            # 如果v不为空字符,加入临时列表
                            value += f",'{v}'"
                        else:
                            # 如果是mysql,设置为空字符,如果是pgsql设置为默认
                            value += ",''" if self.genre == "mysql" else ",DEFAULT"
                # 去掉值中第一个逗号
                value = f"({value[1:]})"
            # 取出键
            key = ",".join(tem_list)

        # 处理表名
        table_name = table_name_process(table, schema, self.schema)

        # 拼接语句
        if self.genre == "mysql":
            sql = f"INSERT IGNORE INTO {table_name} ({key}) VALUES {value}"
        else:
            sql = f"INSERT INTO {table_name} ({key}) VALUES {value} ON CONFLICT DO NOTHING" + \
                f" RETURNING {index}" if index else ""

        return await self.execute_async(sql=sql,  result=result)

    async def delete_async(self, table: str, condition: str = None, schema: str = None, result: dict = {}) -> bool:
        """删除_异步

        Args:
            table (str): 表名
            condition (str): 条件,不填则会清空表
            schema (str, optional): 在mysql中这个参数代表数据库,在pgsql中代表架构. Defaults to None.
            result (dict, optional): 返回对象,包含了数据/错误信息/语句等. Defaults to {}.

        Returns:
            bool: 成功|true 失败|false
        """

        # 如果没有条件,则直接清空
        if not condition:
            return await self.truncate_async(table=table, schema=schema)

        # 处理条件
        condition = condition_process(condition)

        # 处理表名
        table_name = table_name_process(table, schema, self.schema)
        # 拼接语句
        sql = f"DELETE FROM {table_name}{condition}"
        return await self.execute_async(sql=sql,  result=result)

    async def update_async(self, table: str, condition: str = None, kv: str = None, json_data: dict = None, schema: str = None, index: str = None, result: dict = {}) -> bool:
        """更新_异步

        Args:
            table (str): 表名
            condition (str, optional):条件. Defaults to None.
            kv (str, optional): 原参数 a=b,c=d. Defaults to None.
            json_data (dict, optional): 对象参数,如果该参数不为空,kv将失效. Defaults to None.
            schema (str, optional): mysql中为库名,pgsql中为架构. Defaults to None.
            index (str, optional): 仅在pgsql下有效,返回ID. Defaults to None.
            result (dict, optional): 返回对象. Defaults to {}.

        Returns:
            bool: 成功|true 失败|false
        """
        # 对象参数是否存在
        if json_data:
            # 将键值对初始化为空
            kv = ""
            for k, v in json_data.items():
                # 拼接参数
                kv = f"{kv},{k}='{v}'"
            kv = kv[1:]

        # 处理条件
        condition = condition_process(condition)
        # 处理表名
        table_name = table_name_process(table, schema, self.schema)
        # 拼接语句
        sql = f"UPDATE {table_name} SET {kv}{condition}"
        if self.genre == "pgsql":
            sql += f" ON CONFLICT DO NOTHING" + \
                f" RETURNING {index}" if index else ""
        return await self.execute_async(sql=sql, result=result)

    async def select_async(self, table: str, condition: str = None, json_data: dict = None, field: str = "*", limit: str = None, order: str = None, group: str = None, schema: str = None, result: dict = {}) -> bool:
        """查询_异步

        Args:
            table (str): 表名
            condition (str, optional): 条件,json_data不为空时,格式为这样 user_id=`user_id` AND create_time>=`create_time`. Defaults to None.
            json_data (dict, optional): 对象参数. Defaults to None.
            field (str, optional): 字段. Defaults to "*".
            limit (str, optional): 条数. Defaults to None.
            order (str, optional): 排序. Defaults to None.
            group (str, optional): 分组. Defaults to None.
            schema (str, optional): 架构. Defaults to None.
            result (dict, optional): 返回. Defaults to {}.

        Returns:
            bool: _description_
        """
        # 处理条件
        condition = condition_process(condition)
        # 处理表名
        table_name = table_name_process(table, schema, self.schema)
        # 处理过滤
        sql = filter_process(genre=self.genre,
            sql=f"SELECT {field} FROM {table_name}{condition}", group=group, order=order, limit=limit)

        # 如果对象数据不为空,那么就自动替换条件里的参数
        if json_data:
            for key, value in json_data.items():
                sql = sql.replace(f"`{key}`", f"'{value}'")

        return await self.execute_async(sql=sql,  result=result)

    async def truncate_async(self, table: str, schema: str = None, result: dict = {}) -> bool:
        """清空_异步

        Args:
            table (str): 表名
            schema (str, optional): 架构. Defaults to None.

        Returns:
            bool: _description_
        """
        # 处理表名
        table_name = table_name_process(table, schema, self.schema)
        return await self.execute_async(sql=f"TRUNCATE TABLE {table_name}")


async def main():
    db = Database(**json["mysql"])
    await db.connect_async()

    result = {}
    # await db.insert_async(table="users", json_data={
    #           "user_id": "111", "email": "21171193@qq.com"}, result=result)  # 插入
    # print (await db.select_async(table="users", condition="id!=`id`", json_data={"id": 8},limit="1,1", result=result))#查询)
    # await db.update_async(table="users", json_data={
    # "email": "91@qq.com"
    # }, condition="user_id='111'", result=result)
    # print(await db.delete_async(table="users",condition="user_id='p111'" ,result=result))
    await db.truncate_async(table="users", result=result)
    print(result)
    pass

    # result = {}
    # # db.transaction_begin()
    # # db.select(table="users", condition="id=`id`", json_data={"id": 8},limit="1,1", result=result)#查询
    # # db.insert(table="users", json_data={
    #         #   "user_id": "p1111", "email": "3521171193@qq.com"}, result=result)  # 插入

    # # db.update(table="users", json_data={
    # #     "email": "87991@qq.com"
    # # }, condition="user_id='131321'", result=result)
    # print(await db.delete_async(table="users", result=result))
    # # db.transaction_end()
    # print(result)


if __name__ == '__main__':
    # 下面这个是格式模板
    json = {
        "mysql": {
            "schema": "jiejing",
            "password": "123456",
            "pool": True,
            "debug": True,

        },
        "postgreSQL": {
            "user": "tianna",
            "database": "tianna",
            "password": "zl2565809",
            "schema": "tianna",
            "debug": True
        }
    }
    # asyncio.run(main())

    sql = "SELECT interface_id FROM jiejing.interfaces WHERE en='member' LIMIT 1 100 "
    bd = r"LIMIT([\s]+)([\S]+)([\]+)([\s]+)([\w]+)([\s]+)([\d]+)"
    bd = r"LIMIT([\s]+)([\d]+)(,)*[\s]+[\d]+"
    bd = r"LIMIT([\s]+)([\d]+)(,*)([\s]*)([\d]*)"

    print(replace_text(
        sql, bd, ""))
