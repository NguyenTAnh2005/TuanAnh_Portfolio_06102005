from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db_connection import Base

# ======= Bảng thông tin cá nhân ==============
class Myinfo(Base):
    __tablename__ = "myinfos"

    id = Column(Integer, primary_key = True, index = True)
    fullname = Column(String, nullable = False)
    gender = Column(String, nullable = False)
    hometown = Column(String, nullable = False)
    major = Column(String, nullable = False)
    languages = Column(ARRAY(String), nullable = False)
    frameworks = Column(ARRAY(String), nullable = False)
    # Dùng JSONB để lưu các liên kết mạng xã hội linh hoạt
    # Ví dụ: {"github": "link...", "facebook": "link..."}
    social_links = Column(JSONB, nullable = True )
    bio = Column(Text, nullable = True)


#========Bảng ROLE===========
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, unique = True, nullable = False)
    description = Column(String, nullable = True)

    users = relationship("User", back_populates = "role")


# =======Bảng User============
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable = False)

    role = relationship("Role", back_populates = "users")


# =======Bảng Project===========
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key = True, index = True)
    title = Column (String, nullable = False, unique = True)
    description = Column(String, nullable = False)
    thumbnail_url = Column(String, nullable = False)
    project_url = Column(String, nullable = False)
    deploy_url = Column(String, nullable = True)
    #tech_stack = frameworks 
    tech_stack = Column(ARRAY(String), nullable = True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    last_updated = Column(DateTime(timezone=True), nullable=False)


# =======Bảng Category==========
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, unique = True, nullable = False)
    description = Column(String, nullable = True)
    slug = Column(String, unique = True, nullable = False, index = True)

    blogs = relationship("Blog", back_populates = "category")


# =======Bảng Blog============
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False, unique = True)
    summary = Column(String(500), nullable = False)
    content = Column(Text, nullable = False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String, nullable = False, default = "pending")  # pending, published, deleted
    slug = Column (String, unique = True, index = True, nullable = False)
    thumbnail_url = Column(String, nullable = False)
    category = relationship("Category", back_populates = "blogs")


# ======= Bảng Contact Message ========
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key = True, index = True)
    sender_name = Column(String, nullable = False)
    sender_email = Column(String, nullable = False)
    subject = Column(String, nullable = False)
    message = Column(Text, nullable = False)
    status = Column(String, nullable = False, default = "new")  # new, read
    created_at = Column(DateTime(timezone=True), server_default=func.now())


#======== Bảng Config System lưu trữ các cờ quan trọng ====== (hiện tại dùng để lưu cờ đã có dữ liệu mẫu chưa)
class SystemConfig(Base):
    __tablename__="system_configs"

    id = Column(Integer, primary_key = True, index = True)
    config_key = Column(String, unique = True, index = True) # is_seeded
    config_value = Column(String) # True or False or number (string)

