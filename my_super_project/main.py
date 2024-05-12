from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from  sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@app.post("/pay-service/", response_model=dict)
def pay_service(user_email: str, service_name: str, db: Session = Depends(get_db)):
    # Verificar si el usuario existe en la base de datos
    db_user = crud.get_user_by_email(db, email=user_email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Información del servicio a pagar
    service_amount = 5000  # Ejemplo de monto en pesos

    # Llamar a la API para pagar el servicio
    url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
    headers = {
        "Tbk-Api-Key-Id": "597055555532",
        "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        "Content-Type": "application/json"
    }
    payload = {
        "buy_order": f"{user_email}-{service_name}",
        "session_id": f"{user_email}-{service_name}",
        "amount": service_amount,
        "return_url": "http://www.comercio.cl/webpay/retorno"
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        # La solicitud fue exitosa
        return {"message": "Payment request successful", "transaction_details": response.json()}
    else:
        # La solicitud falló
        return {"error": f"Error sending payment request: {response.status_code} - {response.text}"}
