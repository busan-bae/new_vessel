from flask import Blueprint,session,redirect,url_for,request,flash, render_template
from models import db, Vessel, VesselDetail
from routes.decorators import login_required


vessel_bp = Blueprint("vessel",__name__)


@vessel_bp.route("/vessel/new", methods=["GET", "POST"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
def vessel_new():
    
    if request.method == "POST":
        name = request.form.get("name")
        imo_number = request.form.get("imo_number")
        ship_type = request.form.get("ship_type")
        gross_tonnage = request.form.get("gross_tonnage")
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
            gross_tonnage=gross_tonnage, 
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
    
    vessels = Vessel.query.all()  # DB에서 모든 선박 정보 조회
    return render_template("vessel_list.html", vessels=vessels)  # vessel_list.html 템플릿 렌더링


@vessel_bp.route("/vessel/<int:vessel_id>", methods=["GET"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
def vessel_detail(vessel_id):

    
    vessel = Vessel.query.get_or_404(vessel_id)# DB에서 해당 ID의 선박 정보 조회, 없으면 404 에러)   
    return render_template("vessel_detail.html", vessel=vessel)  # vessel_list.html 템플릿 렌더링

@vessel_bp.route("/vessel/<int:vessel_id>/edit", methods=["GET", "POST"])
@login_required # 로그인 여부 확인 -> 비 로그인시 로그인 페이지 이동
def vessel_edit(vessel_id):
    
    vessel = Vessel.query.get_or_404(vessel_id)# DB에서 해당 ID의 선박 정보 조회, 없으면 404 에러)   

    if request.method == "POST":
        name = request.form.get("name")
        imo_number = request.form.get("imo_number")
        ship_type = request.form.get("ship_type")
        gross_tonnage = request.form.get("gross_tonnage")
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
        vessel.gross_tonnage = gross_tonnage
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
