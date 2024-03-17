def horaextra():
    sal = float(input("Digite o Salario Mensal Bruto: "))
    print("\n")
    dia = int(input("Digite o dia da Semana que foi feita a Hora Extra |1-->segunda||2-->terca||3-->quarta||4-->quinta||5-->sexta||6-->sabado||7-->domingo||8-->feriado|:  "))
    print("\n")
    hor = int(input("Quantidade de horas extras feitas: "))
    print("\n")
    sahora = sal / 220
    valor_hora_extra = 0
    
    print(f"Valor Salario Hora: {round(sahora,2)}")
    print("\n")
    if dia == 7 or dia == 8:
        valor_hora_extra = sahora * hor * 2.0
    elif dia != 8 and dia != 7:
        valor_hora_extra = sahora * hor * 1.5
    
    print(f"Valor da(s) Hora(s) Extra(s) Realizada(s): {round(valor_hora_extra,2)}")

horaextra()
