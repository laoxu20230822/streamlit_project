# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker, declarative_base, Session
# from sqlalchemy.exc import SQLAlchemyError
# from typing import Type, TypeVar, List, Optional

# # 声明式基类（用于模型继承）
# Base = declarative_base()
# T = TypeVar('T', bound=Base)  # 泛型类型提示（限制为 Base 的子类）

# class Database:
#     def __init__(self, db_url: str = 'sqlite:///users.db', echo: bool = False):
#         """
#         初始化数据库连接
#         :param db_url: 数据库连接字符串（如 'sqlite:///test.db' 或 'postgresql://user:pass@host/db'）
#         :param echo: 是否打印 SQL 日志
#         """
#         self.engine = create_engine(db_url, echo=echo)
#         self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
#         self._create_tables()  # 初始化时自动创建所有表

#     def _create_tables(self):
#         """根据模型类自动创建数据库表"""
#         Base.metadata.create_all(bind=self.engine)

#     def get_session(self) -> Session:
#         """获取数据库会话（需配合 with 语句使用）"""
#         return self.SessionLocal()

#     def add(self, model: T) -> T:
#         """
#         添加单条记录
#         :param model: 模型实例（如 User(name='张三', age=25)）
#         :return: 保存后的模型实例（包含自增 ID）
#         """
#         with self.get_session() as session:
#             try:
#                 session.add(model)
#                 session.commit()
#                 session.refresh(model)  # 刷新实例以获取数据库生成的字段（如自增 ID）
#                 return model
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 raise ValueError(f"添加记录失败: {str(e)}")

#     def get(self, model_class: Type[T], id: int) -> Optional[T]:
#         """
#         根据 ID 查询单条记录
#         :param model_class: 模型类（如 User）
#         :param id: 记录 ID
#         :return: 模型实例或 None
#         """
#         with self.get_session() as session:
#             return session.get(model_class, id)

#     def list(self, model_class: Type[T], limit: int = 100, offset: int = 0) -> List[T]:
#         """
#         分页查询多条记录
#         :param model_class: 模型类
#         :param limit: 每页数量
#         :param offset: 偏移量（从 0 开始）
#         :return: 模型实例列表
#         """
#         with self.get_session() as session:
#             return session.query(model_class).limit(limit).offset(offset).all()

#     def update(self, model: T) -> T:
#         """
#         更新已有记录（需包含 ID）
#         :param model: 包含新值的模型实例（必须有 ID）
#         :return: 更新后的模型实例
#         """
#         with self.get_session() as session:
#             try:
#                 session.merge(model)  # 合并更新（自动根据主键匹配）
#                 session.commit()
#                 session.refresh(model)
#                 return model
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 raise ValueError(f"更新记录失败: {str(e)}")

#     def delete(self, model_class: Type[T], id: int) -> None:
#         """
#         根据 ID 删除记录
#         :param model_class: 模型类
#         :param id: 记录 ID
#         """
#         with self.get_session() as session:
#             try:
#                 obj = session.get(model_class, id)
#                 if obj:
#                     session.delete(obj)
#                     session.commit()
#             except SQLAlchemyError as e:
#                 session.rollback()
#                 raise ValueError(f"删除记录失败: {str(e)}")

# # 示例：定义数据类（映射数据库表）
# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)
#     age = Column(Integer)

#     # 可选：添加 __repr__ 方便调试（类似 Java data class 的 toString）
#     def __repr__(self):
#         return f"User(id={self.id}, name='{self.name}', age={self.age})"

# # 使用示例
# if __name__ == "__main__":
#     # 初始化数据库（SQLite 示例，会自动创建 example.db 文件）
#     db = Database(db_url='sqlite:///users.db', echo=True)
#     # 1. 添加记录
#     new_user = User(name="张三", age=25)
#     saved_user = db.add(new_user)
#     print(f"新增用户: {saved_user}")  # 输出：User(id=1, name='张三', age=25)

#     # 2. 查询记录
#     fetched_user = db.get(User, id=1)
#     print(f"查询用户: {fetched_user}")  # 输出：User(id=1, name='张三', age=25)

#     # 3. 更新记录
#     fetched_user.age = 26
#     updated_user = db.update(fetched_user)
#     print(f"更新后用户: {updated_user}")  # 输出：User(id=1, name='张三', age=26)

#     # 4. 删除记录
#     db.delete(User, id=1)
#     print("用户已删除")

# def get_customers(self):
#     conn = self.get_connection()
#     c = conn.cursor()
#     c.execute('SELECT * FROM customers')
    
#     # 将查询结果转换为数据类实例
#     customers = [
#         Customer(
#             id=row[0],
#             name=row[1],
#             email=row[2],
#             phone=row[3],
#             created_at=datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
#         ) for row in c.fetchall()
#     ]
    
#     conn.close()
#     return customers
    