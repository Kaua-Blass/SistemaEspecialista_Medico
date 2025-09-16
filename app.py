from flask import Flask, render_template, request
from regras import regras

app = Flask(__name__)

@app.route('/')
def index():
    sintomas = sorted({s for lista in regras.values() for s in lista})
    return render_template("index.html", sintomas=sintomas)

@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    selecionados = request.form.getlist("sintomas")
    
    possiveis = []
    
    for doenca, sintomas_da_doenca in regras.items():
        sintomas_correspondentes = [s for s in sintomas_da_doenca if s in selecionados]
        
        if not sintomas_correspondentes:
            continue
            
        porcentagem = (len(sintomas_correspondentes) / len(sintomas_da_doenca)) * 100
        
        if porcentagem >= 50:
            possiveis.append({
                "doenca": doenca,
                "porcentagem": f"{porcentagem:.0f}",
                "sintomas_correspondentes": [s.replace("_", " ").capitalize() for s in sintomas_correspondentes]
            })
            
    possiveis.sort(key=lambda item: item['porcentagem'], reverse=True)
    
    if not possiveis:
        mensagem = "Nenhum diagnóstico com 50% ou mais de correspondência encontrado."
    else:
        mensagem = None

    return render_template("resultado.html", 
                           selecionados=selecionados, 
                           possiveis=possiveis,
                           mensagem=mensagem,
                           regras=regras)

if __name__ == '__main__':
    app.run(debug=True)