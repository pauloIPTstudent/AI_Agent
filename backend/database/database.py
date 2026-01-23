from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, UserMessage, RefinedMessage, FinalResponse
# Configuração do SQLite
DATABASE_URL = "sqlite:///maestro_system.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Cria as tabelas no banco de dados."""
    Base.metadata.create_all(engine)

def log_interaction(
    original_text: str, 
    refined_text: str, 
    final_text: str, 
    refiner_model: str = "llama3", 
    responder_model: str = "llama3"
) -> UserMessage:
    """
    Persiste o fluxo completo do Maestro no banco de dados de forma atômica.
    """
    session = SessionLocal()
    try:
        # 1. Cria a mensagem original
        user_msg = UserMessage(content=original_text)
        session.add(user_msg)
        session.flush() # Gera o ID de user_msg sem comitar a transação

        # 2. Cria a mensagem refinada vinculada
        refined_msg = RefinedMessage(
            content=refined_text,
            model_name=refiner_model,
            user_message_id=user_msg.id
        )
        session.add(refined_msg)
        session.flush()

        # 3. Cria a resposta final vinculada
        final_res = FinalResponse(
            content=final_text,
            model_name=responder_model,
            refined_message_id=refined_msg.id
        )
        session.add(final_res)

        # Commit de toda a operação
        session.commit()
        
        # Refresh para carregar os dados persistidos (opcional)
        session.refresh(user_msg)
        return user_msg

    except Exception as e:
        session.rollback()
        print(f"Erro ao persistir interação: {e}")
        raise
    finally:
        session.close()

def get_all_interactions():
    """
    Recupera todas as interações com seus textos original, refinado e final.
    Retorna uma lista de dicionários com os dados relacionados.
    """
    session = SessionLocal()
    try:
        # Busca todas as mensagens originais com suas respostas relacionadas
        interactions = session.query(UserMessage).all()
        
        result = []
        for user_msg in interactions:
            # Verifica se há uma mensagem refinada
            if user_msg.refined_version:
                refined_msg = user_msg.refined_version
                # Verifica se há uma resposta final
                if refined_msg.final_response:
                    final_res = refined_msg.final_response
                    result.append({
                        "id": user_msg.id,
                        "original_text": user_msg.content,
                        "original_timestamp": user_msg.timestamp,
                        "refined_text": refined_msg.content,
                        "refined_timestamp": refined_msg.timestamp,
                        "refined_model": refined_msg.model_name,
                        "final_text": final_res.content,
                        "final_timestamp": final_res.timestamp,
                        "final_model": final_res.model_name,
                    })
        
        return result
    except Exception as e:
        print(f"Erro ao recuperar interações: {e}")
        raise
    finally:
        session.close()