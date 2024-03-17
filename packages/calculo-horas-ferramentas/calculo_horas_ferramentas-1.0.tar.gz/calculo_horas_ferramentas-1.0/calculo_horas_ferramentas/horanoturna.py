def horanoturna():
    sal = float(input("Digite o Salario Mensal Bruto: "))
    print("\n")
    horanot = int(input("Quantidade de horas noturnas feitas apartir das 22:00hs: "))
    print("\n")
    sahora = sal / 220
    percentual_Ad_noturno = float(input("Digite o percentual de calculo da Hora Noturna: "))
    valor_hora_noturna = ((((sahora * horanot) * percentual_Ad_noturno)/100)+sahora)
    
    print(f"Valor Salario Hora: {round(sahora,2)}")
    print("\n")
   
    
    print(f"Valor da(s) Hora(s) Noturna(s) Realizada(s): {round(valor_hora_noturna,2)}")

horanoturna()
