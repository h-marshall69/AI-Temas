from logic import *
pip install logic
# Cree nuevas clases, cada una con un nombre o un símbolo que represente cada proposición.
rain = Symbol("rain")  # Esta lloviendo.
hagrid = Symbol("hagrid")  # Harry visitó  a Hagrid
dumbledore = Symbol("dumbledore")  # Harry visito a Dumbledore

# Almacena las proposiciones KB
knowledge = And(  # Comienza con el conectivo lógico "And" porque cada proposición representa un conocimiento que sabemos que es verdadero..

    Implication(Not(rain), hagrid),  # ¬(Esta lloviendo) → (Harry visitó a Hagrid)

    Or(hagrid, dumbledore),  # (Harry visitó a Hagrid) ∨ (Harry visitó Dumbledore).

    Not(And(hagrid, dumbledore)),  # ¬(Harry visitó Hagrid ∧ Harry visitó Dumbledore) i.e. Harry no visitó a ambos Hagrid y Dumbledore.

    dumbledore  # Harry visitó Dumbledore.
    )

def check_all(knowledge, query, symbols, model):
    if not symbols:
        if knowledge.evaluate(model):
            return query.evaluate(model)
        return True
    else:
        remaining = symbols.copy()
        p = remaining.pop()

        model_true = model.copy()
        model_true[p] = True

        model_false = model.copy()
        model_false[p] = False

        return(
            check_all(knowledge, query, remaining, model_true) and
            check_all(knowledge, query, remaining, model_false)
            )
print(check_all(rain))

print(model_check(knowledge, Not(rain))
print(check_all(knowledge, hagrid)
print(check_all(knowledge, Not(hagrid))