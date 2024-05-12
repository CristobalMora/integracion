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

@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item(db=db, item_id=item_id, item_update=item_update)

@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.delete_item(db=db, item_id=item_id)

#############################producto#################################

@app.post("/productos/", response_model=schemas.Producto)
def create_producto(producto: schemas.Producto, db: Session = Depends(get_db)):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    return db_producto

@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.Producto, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    for field, value in producto.dict(exclude_unset=True).items():
        setattr(db_producto, field, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.delete("/productos/{producto_id}", response_model=schemas.Producto)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    db.delete(db_producto)
    db.commit()
    return db_producto

############################# trasnbak #############################################

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