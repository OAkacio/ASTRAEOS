<div align="center">

# 🌌 ASTRAEOS

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](#)
[![Julia Core](https://img.shields.io/badge/Julia-1.9%2B-9558B2?logo=julia&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxxxx.svg)](https://doi.org/10.5281/zenodo.xxxxxxx)
[![Status](https://img.shields.io/badge/Status-Beta_v0.1.0-2EA043)](#)

*O **Astraeos** (ou Atraeu) é um titã grego da astronomia e do crepúsculo, pai das estrelas, dos planetas e dos quatro ventos cardeais: Bóreas, Zéfiro, Noto e Euro.*

</div>

<br>

## 🏛️ Informações Acadêmicas
> **Instituição:** Instituto de Astronomia, Geofísica e Ciências Atmosféricas (IAG) — Universidade de São Paulo (USP) <br>
> **Desenvolvedor:** Victor Moreira Acacio [![ORCID](https://img.shields.io/badge/ORCID-0009--0007--4484--2129-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0007-4484-2129) <br>
> **Orientação:** Profa. Dra. Vera Jatenco Silva Pereira <br>
> **Projeto:** Trabalho de Graduação (TG) — Bacharelado em Astronomia <br>
> **Data:** 2026

---

## 🔭 Sobre o ASTRAEOS

O **ASTRAEOS** foi criado para estudar a física entre a astrofísica estelar teórica e a análise de ambientes exoplanetários. Utilizando uma arquitetura híbrida (Python e Julia), o software permite calcular perfis de vento estelar através de modelos de amortecimento de ondas de Alfvén (Jatenco-Pereira & Opher, 1989), contrastando-os com o clássico vento termo-dirigido de Parker.

Além do estudo do plasma estelar, o ASTRAEOS projeta estes ventos na distância orbital de exoplanetas, calculando a **pressão dinâmica**, os **limites da magnetopausa** e o impacto severo de **Ejeções de Massa Coronal (CMEs)**. Também é dotado de um mapeamento das Zonas Habitáveis clássicas e modernas (Kopparapu et al., 2013).

---

## ✨ Principais Funcionalidades

- 🚀 **Motor Numérico em JULIA:** Algoritmo de busca topológica com integração Runge-Kutta (RK4) escrito em Julia para máxima performance, lidando dinamicamente com as singularidades através das regras de L'Hôpital.
- 🌊 **Modelagem de Ventos:** Suporte a modelos de amortecimento de onda Constante e Ressonante, além da solução de vento térmico puro (Parker Wind).
- 🪐 **Mapa de Habitabilidade:** Visualização polar das fronteiras da Zona Habitável (Recent Venus, Runaway/Moist/Maximum Greenhouse, Early Mars).
- 🛡️ **Escudo Magnetosférico:** Simulação vetorial 2D da magnetosfera do exoplaneta com Dipolo comprimido sob fluxo de plasma quiescente e durante impactos de CME.
- 📊 **Open Science:** Exportação limpa de matrizes `.npz` e `.csv` contendo todas as variáveis físicas e resultados obtidos para reprodutibilidade e plotagem independente.

---

## 📸 Interface e Visualizações

<div align="center">
  <img src="interface/assets/examples/ex.inter.png" width="100%">
  <p><i>Interface do ASTRAEOS. Contém uma região de exibição de gráficos, configurações de parâmetros de ventos estelares, configurações de parâmetros de simulação de exoplanetas e exibição de feedbacks do software.</i></p>
</div>

<br>


<div align="center">
  <img src="interface/assets/examples/ex.mg.png" width="100%">
  <p><i>Simulação 2D vetorial do impacto do plasma na magnetosfera planetária. Curva azul e vermelha representam a magnetosfera do vento quiescente e atingido por CME, respectivamente. Círculo verde e vermelho pontilhados representam limites empíricos terrestres de raio de magnetopausa para os dias atuais e para o periodo paleoarqueano, respectivamente.</i></p>
</div>

<br>

<div align="center">
  <img src="interface/assets/examples/ex.zh.png" width="100%">
  <p><i>Mapa de Zona Habitável com gradiente de densidade normalizada do vento simulado. Círulo vermelho pequeno representa o planeta inserido.</i></p>
</div>

<br>

<div align="center">
  <img src="interface/assets/examples/ex.pl.png" width="100%">
  <p><i>Distribuição de propriedades do plasma normalizadas. Contém curvas de comprimento de amortecimento, velocidade, densidade, fluxo de ondas Alfvén, amplitude e pressão dinâmica do vento.</i></p>
</div>

<br>

<div align="center">
  <img src="interface/assets/examples/ex.vel.png" width="100%">
  <p><i>Perfil de velocidade do vento estelar contendo planetas simulados e zona habitável. Ponto crítico apresentado como ponto avermelhado sobre a curva.</i></p>
</div>

---

## ⚙️ Instalação e Requisitos

### Pré-requisitos
- **Python:** `3.10` ou superior.
- **Julia:** `1.9` ou superior (Necessário pacote `QuadGK`).