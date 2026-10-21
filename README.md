# Clássica Hub

Iniciador gráfico local do ☧ SYSTEMS. Não contém mecanismo de download, não compartilha arquivos de dados e não instala ou atualiza módulos.

Configure os comandos de cada módulo explicitamente em `%LOCALAPPDATA%\ClassicaHub\modules.json`, por exemplo:

```json
{"youtube": ["C:\\Apps\\Classica\\Clássica.exe"], "x": ["C:\\Apps\\ClassicaX\\ClassicaX.exe"]}
```

Se um módulo estiver ausente ou falhar, o outro continua disponível. As atualizações são manuais e individuais, nos projetos de cada módulo.
