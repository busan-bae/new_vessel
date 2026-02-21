from models import db,Vessel, VesselDetail
import json
from app import create_app

app = create_app()

with app.app_context():
    # 1. 기존 데이터 삭제
    VesselDetail.query.delete()
    Vessel.query.delete()
    db.session.commit()
    
    # 2. json 파일 열기
    with open("dummydata/ships.json","r", encoding="utf-8") as f:
        ships = json.load(f)
        
    # 3. 데이터 반복 삽입
    for ship in ships:
        vessel = Vessel(
            name = ship["name"],
            imo_number = ship["imo_no"],
            ship_type = ship["ship_type"],
            ship_size = ship["size"],
            flag = ship["flag"],
        )
    
        detail = VesselDetail(
            ship_code= ship["ship_code"],
            vessel_ro = ship["ro"],
            vessel_class = ship["class"],
            built_year = ship["built_year"],
            team = ship["tic"],
            crew = ship["crew"],
        )
        
        vessel.detail = detail
        db.session.add(vessel)
    
    db.session.commit()
    print(f"저장 완료! 총 {len(ships)}척 등록 되었습니다.")
