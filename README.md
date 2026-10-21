# Clássica Hub

Iniciador gráfico local do ☧ SYSTEMS. Não contém mecanismo de download, não compartilha arquivos de dados e não instala ou atualiza módulos.

Configure os comandos de cada módulo explicitamente em `%LOCALAPPDATA%\ClassicaHub\modules.json`, por exemplo:

```json
{"youtube": ["C:\\Apps\\Classica\\Clássica.exe"], "x": ["C:\\Apps\\ClassicaX\\ClassicaX.exe"]}
```

Se um módulo estiver ausente ou falhar, o outro continua disponível. As atualizações são manuais e individuais, nos projetos de cada módulo.

## Windows 10/11 — versão pronta

Use o ZIP da [versão oficial v1.0.0](https://github.com/tiolusystems/classica-hub/releases/tag/v1.0.0), arquivo `ClassicaHub-1.0.0-Windows-x64.zip`. Extraia **toda a pasta**; não mova o executável isoladamente. Não é necessário instalar Python. O pacote ainda não tem assinatura digital; os releases incluem SHA-256 para conferir a integridade.

O aplicativo pode ser instalado ou atualizado pela opção **Plataformas** do Clássica 2.3.0, quando essa versão estiver publicada. A atualização do módulo é opcional e não altera o Clássica YouTube.
