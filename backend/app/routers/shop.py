from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models import shop as models_shop
from schemas import shop as schemas_shop

router = APIRouter(
    prefix="/shop",
    tags=["Shop, Subscriptions & Payments"]
)

# ==========================================
# 1. VETRINA PRODOTTI
# ==========================================

# Aggiungere un nuovo prodotto alla vetrina (Solo Admin)
@router.post("/products/", response_model=schemas_shop.VetrinaResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: schemas_shop.VetrinaCreate, db: Session = Depends(get_db)):
    db_product = models_shop.Vetrina(
        name=product_data.name,
        descrizione=product_data.descrizione,
        brand=product_data.brand,
        price=product_data.price,
        status=product_data.status,
        stock=product_data.stock,
        image_url=product_data.image_url
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Vedere tutti i prodotti disponibili nello shop
@router.get("/products/", response_model=List[schemas_shop.VetrinaResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models_shop.Vetrina).filter(models_shop.Vetrina.status == True).all()


# ==========================================
# 2. ACQUISTI E PAGAMENTI
# ==========================================

# Simula l'acquisto di un prodotto e genera la ricevuta di pagamento
@router.post("/buy-product/", response_model=schemas_shop.PaymentResponse, status_code=status.HTTP_201_CREATED)
def buy_product(cart_data: schemas_shop.AcquistiCreate, db: Session = Depends(get_db)):
    # Utente finto di test (in attesa dell'autenticazione JWT)
    current_user_id = 1
    
    # 1. Verifichiamo se il prodotto esiste e se è disponibile
    product = db.query(models_shop.Vetrina).filter(models_shop.Vetrina.id == cart_data.id_prodotto).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prodotto non trovato.")
    
    if product.stock < cart_data.quantita:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Stock insufficiente. Disponibili solo {product.stock} pezzi.")

    # 2. Scaliamo lo stock del prodotto
    product.stock -= cart_data.quantita
    
    # 3. Calcoliamo il totale
    total_amount = product.price * cart_data.quantita

    # 4. Registriamo l'acquisto nello storico
    db_acquisto = models_shop.Acquisti(
        id_user=current_user_id,
        id_prodotto=product.id,
        quantita=cart_data.quantita
    )
    db.add(db_acquisto)

    # 5. Generiamo la transazione nella tabella payments
    db_payment = models_shop.Payment(
        user_id=current_user_id,
        amount=total_amount,
        payment_method="Carta", # Di default per il test
        item_type="prodotto",
        item_id=product.id,
        quantity=cart_data.quantita,
        handled_by=None # Acquistato autonomamente dall'app senza passare dalla reception
    )
    db.add(db_payment)
    
    db.commit()
    db.refresh(db_payment)
    return db_payment