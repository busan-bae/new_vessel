from flask import Blueprint, request, jsonify,current_app
from models import db, Vessel, VoyageInfo
from datetime import datetime

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/voyage", methods=['POST'])
def receive_voyage():
    # API key 검증
    key = request.headers.get('X-API-Key')
    if key != current_app.config['API_KEY']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # JSON 파싱 — None이면 400 에러 반환
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    try:
        VoyageInfo.query.delete()
        for item in data:
            vessel_name = item['vessel_name'].replace("H/","HYUNDAI ")
            vessel = Vessel.query.filter_by(name=vessel_name).first()
            vessel_id = vessel.id if vessel else None
            
            voyage = VoyageInfo(vessel_name=vessel_name)
            db.session.add(voyage)
                
            # 값 저장
            voyage.vessel_id = vessel_id
            voyage.voy_no = item['voy_no']
            voyage.line = item['line']
            voyage.teu = item['teu']
            voyage.captain = item['captain']
            voyage.chief_engineer = item['chief_engineer']
            voyage.safety_supervisor = item['safety_supervisor']
            voyage.ops_supervisor = item['ops_supervisor']

            # 중첩 객체 파싱
            voyage.psc_mou_1 = item['psc_inspection']['mou_1']
            voyage.psc_date_1 = item['psc_inspection']['date_1']
            voyage.psc_mou_2 = item['psc_inspection']['mou_2']
            voyage.psc_date_2 = item['psc_inspection']['date_2']

            voyage.last_port = item['last_port']['port']
            voyage.last_etd = item['last_port']['etd']

            voyage.next_port = item['next_port']['port']
            voyage.next_eta = item['next_port']['eta']
            voyage.next_etb = item['next_port']['etb']
            voyage.next_etd = item['next_port']['etd']

            voyage.itinerary = item['itinerary']  
            
            voyage.updated_at = datetime.utcnow()
       
        db.session.commit() 
        return jsonify({'message': 'ok'}), 200   
    
    except Exception as e:
        db.session.rollback()  # 에러 발생 시 DB 변경사항 되돌리기
        return jsonify({'error': 'Internal server error'}), 500