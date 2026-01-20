import asyncio 
from app.db_connection import SessionLocal
from app.models import models
from app.core.config import settings
from app.core.security import hashing_password, parse_github_date
from app.core.github_service import get_reposity_info


#=============== SEED DATA ROLES
def seed_data_roles(db):
    db.add(models.Role(id = 1, name = "Admin", description = "Quản trị hệ thống"))
    db.add(models.Role(id = 2, name = "User", description = "Người dùng thông thường"))
    print(f"🫨  Added roles seed data ....... waiting commit .............")


# ============== SEED DATA USER 
def seed_data_user(db):
    first_admin_password = hashing_password(settings.FIRST_ADMIN_PASSWORD)
    first_admin_email = settings.FIRST_ADMIN_EMAIL
    db.add(models.User(
        id = 1, username = "Admin_Nguyen_05",
        password = first_admin_password,
        email = first_admin_email,
        role_id = 1
        ))
    print(f"🫨  Added admin account seed data ....... waiting commit .............")


# ============ MY INFO SEED DATA 
def seed_data_myinfo(db):
    db.add(models.Myinfo(
        id = 1,
        fullname = "Nguyễn Tuấn Anh",
        gender = "Nam",
        hometown = "Hà Tĩnh, Việt Nam",
        major = "Kỹ sư phần mềm - Solfware Engineer",
        languages = ["Python", "HTML", "CSS", "JavaScript", "C#","Java"],
        frameworks = ["Bootstrap", "Tailwind", "React", "FastAPI", "MVC .Net"],
        social_links = {
            "zalo" : "https://zalo.me/0328884320",
            "github" : "https://github.com/NguyenTAnh2005",
            "email" : "mailto=23050118@student.bdu.edu.vn",
            "facebook" : "https://www.facebook.com/share/14QaznFt8ZF",
            "youtube" : "https://www.youtube.com/@N_T_Anh",
            "instagram" : "https://www.instagram.com/tuananh06102005"
        },
        bio = "Trình độ - kinh nghiệm có thể ít nhưng tinh thần học hỏi thì không bao giờ thiếu!"
    ))
    print(f"🫨  Added my info seed data ....... waiting commit .............")


# ================= PROJECTS SEED DATA 
async def seed_data_projects(db):
    list_projects = [
        {
            "title" : "Quản lý siêu thị với Object Oriented Programming",
            "thumbnail_url" : "https://res.cloudinary.com/df5mtvzkn/image/upload/v1767710892/My_Portfolio/Projects/duan_qly_sieuthiOOPCshap/home_w7qxnf.png",
            "project_url" : "https://github.com/NguyenTAnh2005/duan_qly_sieuthiOOPCshap",
            "deploy_url" : "",
            "tech_stack" : []
        },
        {
            "title" : "Hồ sơ cá nhân",
            "thumbnail_url" : "https://res.cloudinary.com/df5mtvzkn/image/upload/v1767711359/My_Portfolio/Projects/My_First_CV/my-vip-cv_tg8hoh.png",
            "project_url" : "https://github.com/NguyenTAnh2005/My_First_CV",
            "deploy_url" : "https://nguyentanh2005.github.io/My_First_CV/",
            "tech_stack" : []
        },
        {
            "title" : "Web nghe nhạc trực tuyến",
            "thumbnail_url" : "https://res.cloudinary.com/df5mtvzkn/image/upload/v1767711439/My_Portfolio/Projects/STAP_Music/stap-music_ued2w9.png",
            "project_url" : "https://github.com/NguyenTAnh2005/STAP_Music",
            "deploy_url" : "https://nguyentanh2005.github.io/STAP_Music/",
            "tech_stack" : []
        },
        {
            "title" : "Ứng dụng dạy nấu ăn ",
            "thumbnail_url" : "https://res.cloudinary.com/df5mtvzkn/image/upload/v1767711370/My_Portfolio/Projects/Let-Cook/let-cook_ptraje.jpg",
            "project_url" : "https://github.com/NguyenTAnh2005/Let-Cook",
            "deploy_url" : "",
            "tech_stack" : ["SQLite"]
        },
        {
            "title" : "Website bán điện thoại cũ",
            "thumbnail_url" : "https://res.cloudinary.com/df5mtvzkn/image/upload/v1767711413/My_Portfolio/Projects/asp_sellphone/asp-sellphone_siuupw.png",
            "project_url" : "https://github.com/NguyenTAnh2005/asp_sellphone",
            "deploy_url" : "http://oldphone.somee.com/",
            "tech_stack" : ["Bootstrap, SweetAlert, Asp .Net, Cloudianry, SQL Sever"]
        },
        {
            "title" : "Ứng dụng theo dõi thói quen",
            "thumbnail_url" : "https://res.cloudinary.com/df5mtvzkn/image/upload/v1767711400/My_Portfolio/Projects/Habit_Tracker/habit-tracker_f9lo64.png",
            "project_url" : "https://github.com/NguyenTAnh2005/Habit_Tracker",
            "deploy_url" : "https://habit-tracker-kappa-gold.vercel.app/",
            "tech_stack" : ["FastAPI", "PostgreSQL", "JWT", "SQLalchemy", "Alembic Migration", "React", "Tailwind", "React-router-DOM", "Lucide React", "ChartJS", "React Calendar Heatmap", "React Tooltip"]
        },
# {PostgreSQL,Mako,HTML,FastAPI,"Lucide React",Python,"React Toolip",JavaScript,CSS,JWT,ChartJS,"React Calender Heatmap",SQLalchemy,"Alembic Migration",React-router-DOM,React,Tailwind}
    ]
    for project in list_projects:
        github_info = await get_reposity_info(project["project_url"])

        if github_info:
            
            final_tech = project["tech_stack"].copy()
            for tech in github_info["tech_stack"]:
                if tech not in final_tech:
                    final_tech.append(tech)

            added_project = models.Project(
                title = project["title"],
                description = github_info["description"],
                thumbnail_url = project["thumbnail_url"],
                project_url = project["project_url"],
                deploy_url = project["deploy_url"],
                tech_stack = final_tech,
                created_at = parse_github_date(github_info["created_at"]),
                last_updated = parse_github_date(github_info["last_updated"])
            )
            db.add(added_project)
    print(f"🫨  Added projects seed data ....... waiting commit .............")


# ============ CATEGORY SEED DATA 
def seed_data_category_blogs(db):
    categories = [
        {"id" : 1,"name": "Học tập", "slug": "hoc-tap--hocthuat", "description": "Chia sẻ kiến thức, kinh nghiệm trong quá trình học tập chính"},
        {"id" : 2,"name": "Giải trí", "slug": "giaitri-thethao", "description": "Chia sẻ xung quanh về giải trí, thể thao"},
        {"id" : 3,"name": "Đời sống", "slug": "life", "description": "Chia sẻ các câu chuyện xung quanh đời sống"},
        {"id" : 4,"name": "Kiến thức", "slug": "other--learning", "description": "Chia sẻ các kiến thức ngoài lĩnh vực đang học tập"},
        {"id" : 5,"name": "Khác", "slug": "other", "description": "Lĩnh vực chưa được phân loại"},
    ]
    for cat in categories:
        db.add(models.CategoryBlog(**cat))
    print(f"🫨  Added category_blogs seed data ....... waiting commit .............")


#================= BLOGS SEED DATA
def seed_data_blogs(db):
    blog_1_content = """
    Đó là thời điểm vào học kỳ đầu tiên của năm học thứ 3. Cũng là thời điểm sau 6 tháng mình làm quen với bộ ba cơ bản HTML-CSS-JavaScript.
     Đây là dự án cho môn học phát triển ứng dụng mã nguồn mở. Và đương nhiên, đây là lần đầu bản thân mình thực sự code một dự án fullstack nên chắc chắn vẫn còn khá nhiều thứ thiếu sót. 
     Tuy nhiên đối với bản thân mình thì đây là dự án thứ 2 mà bản thân mình thực sự tâm đắc (dự án đầu tiên là một CV sau nửa học kỳ làm quen với html-css-js). 
     Dự án được giảng viên yêu cầu bắt buộc backend cần dùng FastAPI kết hợp JWT và dùng PostgreSQL, đây cũng là phần mình code nhiều hơn là frontend - phần giảng viên cho phép dùng AI hỗ trợ. 
     Ở frontend dự án này thì mình dùng React với Vite. Dự án được mô tả là sẽ theo dõi thói quen của người dùng, thống kê lịch sử checkin các thói quen cũng như biểu hiện ra các sơ đồ trực quan (hình tròn, cột).
     Thời điểm này cũng có khá nhiều môn học cùng có dự án cuối kỳ nên thực sự thời gian để dành cho dự án này là không hề nhiều, với đối với một người chân ướt chân ráo - chưa có kinh nghiệm nhiều về code một web đầy đủ frontend - backend,
     thì đây thực sự là một khó khăn. Tuy nhiên, với công nghệ trí tuệ nhân tạo càng ngày phát triển, ngoài các kiến thức giảng viên cung cấp trên lớp học, thì mình cũng dùng một AI chat - Gemini Pro 2.5+, với sự hỗ trợ 
     của nó đã giúp mình hiểu hơn về quy trình thực hiện backend - từ việc xây dựng CSDL, tạo các models, triển khai các API endpoint, tích hợp JWT, xây dựng CORC, kết nối backend - frontend. Và gần như 90% code frontend đều 
     được AI này code <hộ>, tuy nhiên phần này giảng viên không yêu cầu mình phải code, chủ yếu giảng viên chỉ yêu cầu về backend hơn là front. Dù dự án khá thành công nhưng tồn tại song song một số điểm còn thiếu về dự án cũng 
     như cách mình triển khai code web fullstack. Đây sẽ là một động lực thúc đẩy bản thân mình có thể phát triển nhiều hơn. Và trước hết là mình sẽ triển khai một dự án Portfolio - cũng dùng các công cụ như trên. Mục đích là để
     có thể củng cố lại kiến thức backend như trên và quan trọng là nắm vững React căn bản nhất cho một frontend thay vì copy patse như frontend dự án habit-tracker này.
"""
    db.add(models.Blog(
            title="Dự án fullstack đầu tiên và ổn áp nhất của tôi!",
            slug="du-an-fullstack--first",
            summary="Bài viết chia sẻ hành trình bản thân mình code một dự án fullstack đầu tiên và oke nhất!",
            content= blog_1_content,
            category_blog_id = 1,
            status="published",
            thumbnail_url="https://res.cloudinary.com/df5mtvzkn/image/upload/v1767752471/My_Portfolio/Blogs/blog__1/Habit_Tracker_qht1gv.png"
        ))
    print(f"🫨  Added blogs seed data ....... waiting commit .............")

# ================= CATEGORY ACHIEVEMENT SEED DATA
def seed_data_category_achievement(db):
    categories = [
        {"id" : 1,"name": "CNTT", "description": "Thành tích liên quan chuyên ngành"},
        {"id" : 2,"name": "Ngoại ngữ", "description": "Thành tích ngoại ngữ"},
        {"id" : 3,"name": "Khác", "description": "Khác - Anh khạc hay em khạc"}
    ]
    for cat in categories:
        db.add(models.CategoryAchievement(**cat))
    print(f"🫨  Added category_achievements seed data ....... waiting commit .............")

# ================= TIMELINE SEED DATA
def seed_data_timeline(db):
    timelines = [
        {
            "id": 1,
            "title": "Sinh viên đại học",
            "organization": "Trường đại học Bình Dương",
            "description": "Quãng thời gian tuyệt vời, cách thức học khác lạ so với các cấp dưới, tôi làm quen được nhiều bạn bè hơn, cởi mở trong xã hội hơn. Từ những ngày chập chững trong học tập lẫn sinh sống, ngày qua ngày tôi dần thích nghi và đắm chìm trong quãng thời gian học đường tuyệt vời này. Hên là chưa tạch môn.",
            "start_end": "2023 - Hiện nay",
            "sort_order": 1
        },
        {
            "id": 2,
            "title": "Đi làm thêm ở GS25",
            "organization": "Chung cư Opal Skyline tại Bình Dương.",
            "description": "Trải nghiệm đi làm thêm tại cửa hàng tiện lợi GS25 - chuỗi cửa hàng có nguồn gốc từ Hàn Quốc. Tại đây tôi có nhiều trải nghiệm quý giá và cảm thấy trân trọng đồng tiền hơn. Nhưng tôi chỉ làm được vỏn vẹn 6 tháng trong năm hai tại đại học do không thể dành thêm thời gian tối thiểu trong tuần để đi làm.",
            "start_end": "12/2024 - 06/2025",
            "sort_order": 2
        },
        {
            "id": 3,
            "title": "Học sinh phổ thông",
            "organization": "Trường THPT Cẩm Bình",
            "description": "Một quãng thời gian học tập khá bình thường, không quá giỏi giang cũng không kém, thành tích học tập khá ổn. Thời điểm năm học lớp 11 (2021 - 2022), tôi được tiếp cận ngôn ngữ đầu tiên là PASCAL, lúc này tôi cũng chưa có một laptop để học lập trình.",
            "start_end": "2020 - 2023",
            "sort_order": 3
        },
        {
            "id": 4,
            "title": "Học sinh trung học",
            "organization": "Trường THCS Nguyễn Hữu Thái",
            "description": "Một khoảng thời gian học tập khá tuyệt vời, nơi kiến thức chưa nhiều và tôi cũng từng đi thi HSG huyện môn Toán 3 năm, Hóa 1 năm nhưng đều không thành công dù chỉ một giải khuyến khích :(",
            "start_end": "2016 - 2020",
            "sort_order": 4
        },
        {
            "id": 5,
            "title": "Học sinh tiểu học",
            "organization": "Trường tiểu học Cẩm Quang",
            "description": "Thời gian học cấp một tại trường học cũng quê nhà.",
            "start_end": "2011 - 2016",
            "sort_order": 5
        },
    ]

    for time in timelines:
        db.add(models.Timeline(**time))

    print(f"🫨  Added timelines seed data ....... waiting commit .............")

async def seed_data():
    db = SessionLocal()
    '''
    Checking first the flag in database, if has added Seed data, pass and ngược lại
    is_seeded = true or false
    '''
    try:
        check_is_seeded = db.query(models.SystemConfig).filter_by(config_key = "is_seeded").first()
        if check_is_seeded and check_is_seeded.config_value == "true":
            print(f"😑  Seed data has been added before!!!!!!")
            return
        
        print(f"⏰ 🌱 Starting add seed data.............")
        seed_data_roles(db)
        seed_data_user(db)
        seed_data_myinfo(db)
        seed_data_category_blogs(db)
        seed_data_blogs(db)
        seed_data_timeline(db)
        await seed_data_projects(db)
        
        if check_is_seeded:
            check_is_seeded.config_value = "true"
        else:
            added_config = models.SystemConfig(config_key = "is_seeded", config_value = "true")
            db.add(added_config)

        db.commit()

        print(f"✅ 🗿 Added and commited seed data was successfully! 36")

    except Exception as E:
        db.rollback()
        print(f"😭 Oppps, Error: {E}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
