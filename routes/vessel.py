from flask import Blueprint,session,redirect,url_for,request,flash, render_template
from models import db, Vessel, VesselDetail,VoyageInfo
from routes.decorators import login_required, admin_required


vessel_bp = Blueprint("vessel",__name__)


@vessel_bp.route("/vessel/new", methods=["GET", "POST"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
@admin_required  
def vessel_new():
    
    if request.method == "POST":
        name = request.form.get("name")
        imo_number = request.form.get("imo_number")
        ship_type = request.form.get("ship_type")
        ship_size = request.form.get("ship_size")
        flag = request.form.get("flag")
        

        ship_code = request.form.get("ship_code")
        vessel_ro = request.form.get("vessel_ro")
        vessel_class = request.form.get("vessel_class")
        built_year = request.form.get("built_year")
        team = request.form.get("team")
        crew = request.form.get("crew")
        
    
        
        if Vessel.query.filter_by(imo_number=imo_number).first():
            flash("이미 등록된 IMO 번호입니다.", "error")
        elif Vessel.query.filter_by(name=name).first():
            flash("이미 등록된 선박 이름입니다.", "error")    
        else:
            new_vessel = Vessel(
            name=name, 
            imo_number=imo_number, 
            ship_type=ship_type, 
            ship_size=ship_size, 
            flag=flag
            )
            
            new_vessel_detail = VesselDetail(
            ship_code=ship_code,
            vessel_ro=vessel_ro,
            vessel_class=vessel_class,
            built_year=built_year,
            team = team,
            crew = crew
            ) 
            
            new_vessel.detail = new_vessel_detail  # Vessel과 VesselDetail 연결
            
            db.session.add(new_vessel)
            db.session.commit()
            flash("선박 등록이 완료되었습니다.", "success")
            return redirect(url_for("vessel.vessel_list"))  # 선박 등록 후 선박 목록 페이지로 리디렉션
    
    return render_template("vessel_new.html")
    

@vessel_bp.route("/vessel/list", methods=["GET"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
def vessel_list():
    # 1. URL 쿼리 파라미터에서 검색조건 읽기
    name = request.args.get("name","")
    ship_type = request.args.get("ship_type","")
    flag = request.args.get("flag","")

    # 2. 기본 쿼리 시작
    query = Vessel.query
    
    # 3. 조건이 있으면 필터 추가
    if name:
        query = query.filter(Vessel.name.like(f"%{name}%"))
    if ship_type:
        query = query.filter_by(ship_type=ship_type)
    if flag:
        query = query.filter_by(flag=flag)
    
    
        
    # vessels = query.all()
    # 위 코드가 아래처럼 페이지 네이션 됨
    
    page = request.args.get("page",1,type=int) # url에서 페이지 번호 읽기
    pagination = query.paginate(page=page, per_page=20 , error_out=False)
    vessels = pagination.items
    
    
    # 4. 최종 실행
    return render_template("vessel_list.html", vessels=vessels, name=name, ship_type=ship_type,flag=flag,pagination=pagination)  # vessel_list.html 템플릿 렌더링


@vessel_bp.route("/vessel/<int:vessel_id>", methods=["GET"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
def vessel_detail(vessel_id):

    
    vessel = Vessel.query.get_or_404(vessel_id)# DB에서 해당 ID의 선박 정보 조회, 없으면 404 에러)   
    return render_template("vessel_detail.html", vessel=vessel)  # vessel_list.html 템플릿 렌더링

@vessel_bp.route("/vessel/<int:vessel_id>/edit", methods=["GET", "POST"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
@admin_required
def vessel_edit(vessel_id):
    
    vessel = Vessel.query.get_or_404(vessel_id)# DB에서 해당 ID의 선박 정보 조회, 없으면 404 에러)   

    if request.method == "POST":
        name = request.form.get("name")
        imo_number = request.form.get("imo_number")
        ship_type = request.form.get("ship_type")
        ship_size = request.form.get("ship_size")
        flag = request.form.get("flag")
        
        ship_code = request.form.get("ship_code")
        vessel_ro = request.form.get("vessel_ro")
        vessel_class = request.form.get("vessel_class")
        built_year = request.form.get("built_year")
        team = request.form.get("team")
        crew = request.form.get("crew")
        
        vessel.name = name
        vessel.imo_number = imo_number
        vessel.ship_type = ship_type
        vessel.ship_size = ship_size
        vessel.flag = flag
        vessel.detail.ship_code = ship_code
        vessel.detail.vessel_ro = vessel_ro
        vessel.detail.vessel_class = vessel_class
        vessel.detail.built_year = built_year
        vessel.detail.team = team
        vessel.detail.crew = crew
        
        vessel.detail.vessel = vessel
        db.session.commit()
        flash("선박 정보가 수정되었습니다.","success")
        return redirect(url_for("vessel.vessel_detail", vessel_id=vessel.id))  # 수정 후 선박 상세 페이지로 리디렉션
    
    return render_template("vessel_edit.html", vessel=vessel)  # vessel_edit.html 템플릿 렌더링

@vessel_bp.route("/vessel/<int:vessel_id>/delete", methods=["POST"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
@admin_required
def vessel_delete(vessel_id):
      
    vessel = Vessel.query.get_or_404(vessel_id)# DB에서 해당 ID의 선박 정보 조회, 없으면 404 에러)   
    
    try:
        db.session.delete(vessel.detail)
    except:
        pass
        
    db.session.delete(vessel)
    db.session.commit()
    flash("선박 정보가 삭제되었습니다.","success")
    return redirect(url_for("vessel.vessel_list"))


@vessel_bp.route("/voyage" , methods=["GET"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
def voyage_list():
    vessel_name = request.args.get("vessel_name", "")
    line = request.args.get("line", "")
    s_crew = request.args.get("s_crew", "")
    supervisor = request.args.get("supervisor", "")
    
    query = VoyageInfo.query
    
    if vessel_name:
        query = query.filter(VoyageInfo.vessel_name.like(f"%{vessel_name}%"))
    if line:
        query = query.filter(VoyageInfo.line.like(f"%{line}%"))
    if supervisor:
          # 담당감독 또는 운항감독 중 하나라도 일치하면 검색
        query = query.filter(
            (VoyageInfo.safety_supervisor.like(f"%{supervisor}%")) |
            (VoyageInfo.ops_supervisor.like(f"%{supervisor}%"))
          )
    if s_crew:
        query =query.filter(
            (VoyageInfo.captain.like(f"%{s_crew}%")) |
            (VoyageInfo.chief_engineer.like(f"%{s_crew}%"))
        )
               
    # voyages = query.order_by(VoyageInfo.vessel_name).all() 
    page = request.args.get("page",1,type=int)
    pagination = query.order_by(VoyageInfo.vessel_name).paginate(page=page, per_page=20, error_out=False)   
    voyages = pagination.items
    
    return render_template("voyage_list.html",voyages=voyages,
                           vessel_name=vessel_name, s_crew=s_crew,
                           line=line, supervisor=supervisor, pagination=pagination)



@vessel_bp.route("/voyage/<int:voyage_id>" , methods=["GET"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
def voyage_detail(voyage_id):
    # VoyageInfo 테이블에서 해당 ID 조회, 없으면 404
    voyage = VoyageInfo.query.get_or_404(voyage_id)
    return render_template("voyage_detail.html",voyage=voyage)

