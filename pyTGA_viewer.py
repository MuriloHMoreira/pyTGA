import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# Caminho do arquivo CSV
name = 'Ensaio_teste10CACsemfibra1'


##################################################
##################################################
##################################################
# Nao esquecer de salvar
##################################################
##################################################
##################################################
# Nao precisa editar nada abaixo
##################################################
##################################################
##################################################


csv_path = f"./Vitória de Alencar/{name}.csv"  # coloque o caminho correto aqui

# Configuração inicial do gráfico
fig, ax1 = plt.subplots(figsize=(9, 6))
plt.ion()  # modo interativo

ax2 = ax1.twinx()  # segundo eixo y
axs = [ax1, ax2]

# Linhas do gráfico
line1_PV, = ax1.plot([], [], '-o', c='navy', label='Temp. Controlador')
line2_SP, = ax1.plot([], [], '-^', c='dodgerblue', label='Temp. Programa')
line3_F,  = ax1.plot([], [], '-^', c='orangered', label='Temp. Forno')
line4_S,  = ax1.plot([], [], '-^', c='goldenrod', label='Temp. Amostra')
line5_m,  = ax2.plot([], [], '-^', c='k', label='Massa')

ax1.set_xlabel('Tempo [s]')
ax1.set_ylabel('Temperatura [°C]')
ax2.set_ylabel('Massa [g]')

axs[0].grid(True)

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.subplots_adjust(wspace=0.3)
plt.show()

# Função para ler o CSV de forma segura
def read_csv_safe(path):
    try:
        df = pd.read_csv(path,  delim_whitespace=True, encoding='ISO-8859-1', engine='python')
        return df
    except:
        pass

# Loop de atualização
print("Iniciando leitura em tempo real do CSV...\n")
while True:
    df = read_csv_safe(csv_path)
    if df is not None and len(df) > 0:
        # Espera-se que o CSV tenha colunas: t, m, PV, SP, F, S
        try:
            ts = df.iloc[:, 0]
            m_reads = df.iloc[:, 1]
            PV_reads = df.iloc[:, 2]
            SP_reads = df.iloc[:, 3]
            F_reads = df.iloc[:, 4]
            S_reads = df.iloc[:, 5]
        except Exception as e:
            print("Erro ao processar colunas:", e)
            time.sleep(1)
            continue

        # Atualiza os dados das linhas
        line1_PV.set_data(ts, PV_reads)
        line2_SP.set_data(ts, SP_reads)
        line3_F.set_data(ts, F_reads)
        line4_S.set_data(ts, S_reads)
        line5_m.set_data(ts, m_reads)

        # Redimensiona e redesenha o gráfico
        for ax in axs:
            ax.relim()
            ax.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()

    else:
        print("Aguardando dados no CSV...")

    time.sleep(1)
