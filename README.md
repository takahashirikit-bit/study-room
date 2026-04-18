# 📚 study-room

日々の技術学習のログと検証コードを一元管理するリポジトリです。
低レイヤーからアプリ層、インフラまでを体系的に管理し、AIによる学習支援機能を組み込んでいます。

## 🎯 目的
- **垂直統合的な学習**: OS/Linuxカーネル、アプリ開発(Flutter/Unity)、インフラ(IaC/CI/CD)を横断的に理解する。
- **AIによる学習支援**: GitHub Actions × Gemini APIを活用し、学習メモの要約とクイズを自動生成する。

## 📂 ディレクトリ構成
- **00_meta**: 学習計画・ロードマップ
- **01_core**: 低レイヤー・基盤技術 (Linux / OS自作)
- **02_arch**: 設計・アーキテクチャ
- **03_apps**: アプリ開発 (Flutter / Unity / Shaders)
- **04_infra**: インフラ・CI/CD (Terraform / GitHub Actions)
- **scripts**: 自動化・補助スクリプト

## ✨ 自動化の仕組み (AI Study Automation)
Issueに学習内容を記録すると、GitHub Actionsが起動して以下を自動実行します。
1. **要約生成**: Gemini APIが内容を簡潔にまとめ。
2. **理解度クイズ**: 復習用のクイズを自動生成してコメント。

## 🛠 注力技術
- **DevOps**: GitHub Actions, Terraform, CI/CD最適化
- **App/Graphics**: Flutter, Unity (SRP, Shader)
- **Low-Level**: C, Linux Kernel, Debugger
