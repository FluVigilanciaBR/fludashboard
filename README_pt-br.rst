============
InfoGripe
============

InfoGripe é uma iniciativa para monitorar e apresentar níveis de alerta para os casos reportados de Síndrome Respiratória Aguda Grave (SRAG) no SINAN, o Sistema de Informação de Agravos de Notificação (www.saude.gov.br/sinan).
Os dados são apresentados por estado e por regiões de vigilância para síndromes gripais.

Este é um produto da parceria entre pesquisadores do Programa de Computação Científica da Fundação Oswaldo Cruz (Fiocruz, PROCC), da Escola de Matemática Aplicada da Fundação Getúlio Vargas (FGV, EMAp), no Rio de Janeiro, e do GT-Influenza da Secretaria de Vigilância Sanitária do Ministério da Saúde (GT-Influenza, SVS, MS).

* Software livre: GNU General Public License v3
* Documentação: https://fludashboard.readthedocs.io.


Funcionalidades
---------------

* Nowcast de incidência semanal;
* Limiares de atividade;
* Distribuição etária dos casos notificados;
* Nível de atividade por temporada;
* Séries históricas.

Tutoriais
---------

* Panorama semanal:

  https://youtu.be/OWbvpxsJnpQ

.. youtube:: OWbvpxsJnpQ


=============================
Descrição das funcionalidades
=============================

InfoGripe apresenta níveis de atividade e informação sobre a série temporal de incidência por semana epidemiológica (SE) e por temporada.
Estas informações podem ser visualizadas pelo panorama **Detalhado (semana)** e **Resumido (ano)**. Cada panorama é composto por quatro painéis:

- Mapa do país;
- Curva de incidência (por 100mil habitantes);
- Tabela de incidência (por 100mil habitantes);
- Distribuição etária (por 100mil habitantes);

Em cada panorama, as informações podem ser visualizadas por estado (UF) ou região.

Panorama Detalhado (semana):
----------------------------

- Mapa do país (superior esquerdo)

 Cada estado/região possui uma cor de acordo com o nível de atividade para a SE selecionada:

 - Atividade baixa (verde): incidência abaixo do limiar pré-epidêmico;
 - Atividade epidêmica (amarelo): incidência acima do limiar pré-epidêmico e abaixo do limiar de atividade alta;
 - Atividade alta (laranja): incidência acima do limiar de atividade alta e abaixo do de atividade muito alta;
 - Atividade muito alta (vermelho): incidência acima do limiar de atividade muito alta.

- Curva de incidência (superior direito)

 Este painel apresenta a série temporal de incidência reportada (curva preta sólida) para a temporada correspondente, com uma linha vertical indicando a SE selecionada. Estimativas de incidência, quando disponíveis, são apresentadas com curva sólida em vermelho, com o intervalo de confiança de 95% representado por linhas vermelhas pontilhadas. A probabilidade de cada nível de atividade também é apresentado em formato de texto no canto superior esquerdo do gráfico. As cores do mapa correspondem ao nível de maior probabilidade. Além da incidência, neste gráfico apresentamos também os limiares de atividade correspondente:

 - Limiar pré-epidêmico (linha azul tracejada): nível de atividade que indica, quando ultrapassado, o início da transmissão sustentada para a temporada atual. Após superar este limiar, a incidência tende a apresentar crescimento gradual até atingir o pico de incidência para aquele ano;
 - Limiar de atividade alta (linha verde tracejada): nível de atividade a partir do qual a incidência é considerada alta para aquela localidade (estado/região). Calculado com base em estimativa para o percentil 90 da distribuição de incidência semanal histórica;
 - Nível de atividade muito alta (linha vermelha tracejada): nível de atividade a partir da qual a incidência é considerada muito elevada para aquela localidade. Calculado com base na estimativa para o percentil 97.5 da distribuição de incidência semanal histórica;

- Esquema de cores do pano de fundo da curva de incidência

 O pano de fundo demarca os níveis de atividade típicos para cada semana. Isto é, o perfil histórica da incidência para cada semana. Isto permite indetificar o padrão sazonal típico , facilitando a identificação do período usual de atividade epidêmica.

 - Atividade semanal baixa (área verde): incidência abaixo do percentil 10 para cada SE;
 - Atividade semanal baixa à moderada (área amarela): incidência entre os percentís 10 e 50 (mediana) para cada SE;
 - Atividade semanal moderada à alta (área laranja): incidência entre os percentís 50 e 90 para cada SE;
 - Atividade semanal alta (área vermelha): incidência acima do percentil 90 para cada SE.

 Quando a incidência em uma determinada semana está dentro da região de atividade alta (fundo vermelho), indica que para aquela SE a atividade é atípicamente alta, independentemente dos limiares de atividade. Esta informação é útil para detectar temporadas em que o período epidêmico se inicia antes do usual, por exemplo. Vê a temporada de 2016 no estado do Rio Grande do Sul para um exemplo deste comportamento.

- Tabela de incidência (inferior esquerdo)

 Incidência para a localidade correspondente na SE selecionada, juntamente com o intervalo de confiança de 90% quando valor for estimado. Juntamenteda incidência e nome da localidade, esta tabela apresenta a situação dos dados selecionados:

 - Estável: dados reportados considerados suficientemente próximos do total casos notificados. Estes dados estão sujeitos a pequenas alterações futuras;
 - Estimado: dados reportados baseado em estimativa para a oportunidade de digitação. Isto é, baseado no número de notificações já digitadas no sistema (dados incompletos) e o tempo típico entre notificação na unidade de saúde e digitação desta notificação no sistema. Estes dados podem sofrer alterações futuras, tornando-se estáveis após algumas semanas;
 - Incompleto: dados reportados ainda não são estáveis em função do padrão de oportunidade de digitação observado na localidade selecionada e nosso sistema não é capaz de produzir estimativas confiáveis. Estes dados podem sofrer grandes alterações futuras, tornando-se estáveis após algumas semanas.

- Distribuição etária e por gênero (inferior direito)

 Gráfico de barras para a incidência reportada (sem uso de estimativa) por faixa etária e gênero, para a SE selecionada.

 - Mulheres: barra azul;
 - Homens: barra laranja;
 - Total: barra verde

 Estas distribuições estão sujeitas a alterações conforme situação reportada na tabela de incidência. Neste painel não apresentamos estimativas por faixa etária, reportando apenas as notificações já digitadas, sejam os dados estáveis ou incompletos.


Panorama Resumido (ano):
------------------------

Este panorama apresenta a situação anual com base nos níveis de atividade descritos no panorama detalhado.

- Mapa do país (superior esquerdo)

 Cada localidade apresenta cor de acordo com a atividade regsitrada na temporada selecionada seguindo os seguintes critérios:

 - Atividade baixa (verde): incidência abaixo do limiar pré-epidêmico durante toda a temporada;
 - Atividade epidêmica (amarelo): incidência superou o limiar pré-epidêmico ao menos em uma SE porém não superou o limiar de atividade alta;
 - Atividade alta (laranja): incidência superou o limiar de atividade alta ou muito alta entre 1 a 4 SEs;
 - Atividade muito alta (vermelho): incidência superou o limiar de atividade alta ou muito alta em ao menos 5 SEs.

- Curva de incidência (superior direito)

 Este painel apresenta a série temporal de incidência reportada (curva preta sólida) para a temporada correspondente. Estimativas de incidência, quando disponíveis, são apresentadas com curva sólida em vermelho, com o intervalo de confiança de 95% representado por linhas vermelhas pontilhadas. A probabilidade de cada nível de atividade também é apresentado em formato de texto no canto superior esquerdo do gráfico. As cores do mapa correspondem ao nível de maior probabilidade. Além da incidência, neste gráfico apresentamos também os limiares de atividade correspondente:

 - Limiar pré-epidêmico (linha azul tracejada): nível de atividade que indica, quando ultrapassado, o início da transmissão sustentada para a temporada atual. Após superar este limiar, a incidência tende a apresentar crescimento gradual até atingir o pico de incidência para aquele ano;
 - Limiar de atividade alta (linha verde tracejada): nível de atividade a partir do qual a incidência é considerada alta para aquela localidade (estado/região). Calculado com base em estimativa para o percentil 90 da distribuição de incidência semanal histórica;
 - Nível de atividade muito alta (linha vermelha tracejada): nível de atividade a partir da qual a incidência é considerada muito elevada para aquela localidade. Calculado com base na estimativa para o percentil 97.5 da distribuição de incidência semanal histórica;

- Esquema de cores do pano de fundo da curva de incidência

 O pano de fundo demarca os níveis de atividade típicos para cada semana. Isto é, o perfil histórica da incidência para cada semana. Isto permite indetificar o padrão sazonal típico , facilitando a identificação do período usual de atividade epidêmica.

 - Atividade semanal baixa (área verde): incidência abaixo do percentil 10 para cada SE;
 - Atividade semanal baixa à moderada (área amarela): incidência entre os percentís 10 e 50 (mediana) para cada SE;
 - Atividade semanal moderada à alta (área laranja): incidência entre os percentís 50 e 90 para cada SE;
 - Atividade semanal alta (área vermelha): incidência acima do percentil 90 para cada SE.

 Quando a incidência em uma determinada semana está dentro da região de atividade alta (fundo vermelho), indica que para aquela SE a atividade é atípicamente alta, independentemente dos limiares de atividade. Esta informação é útil para detectar temporadas em que o período epidêmico se inicia antes do usual, por exemplo. Vê a temporada de 2016 no estado do Rio Grande do Sul para um exemplo deste comportamento.

- Tabela de incidência (inferior esquerdo)

 Incidência para a localidade correspondente na temporada selecionada, juntamente com o intervalo de confiança de 90% quando valor for estimado. Juntamenteda incidência e nome da localidade, esta tabela apresenta a situação dos dados selecionados:

 - Estável: dados reportados considerados suficientemente próximos do total casos notificados. Estes dados estão sujeitos a pequenas alterações futuras;
 - Incompleto: dados reportados ainda não são estáveis em função do padrão de oportunidade de digitação observado na localidade selecionada e nosso sistema não é capaz de produzir estimativas confiáveis. Estes dados podem sofrer grandes alterações futuras, tornando-se estáveis após algumas semanas.

- Distribuição etária e por gênero (inferior direito)

  Gráfico de barras para incidência reportada (sem uso de estimativa) por faixa etária e gênero, para a temporada selecionada.

 - Mulheres: barra azul;
 - Homens: barra laranja;
 - Total: barra verde

 Estas distribuições estão sujeitas a alterações conforme situação reportada na tabela de incidência. Neste painel não apresentamos estimativas por faixa etária, reportando apenas as notificações já digitadas, sejam os dados estáveis ou incompletos.