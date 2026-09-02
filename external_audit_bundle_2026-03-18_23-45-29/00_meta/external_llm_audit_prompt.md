# External LLM Audit Prompt

Проведи независимый архитектурный аудит моей локальной AI-системы как опытный CTO / enterprise architect / AI systems architect.

Контекст:
- Я строю персональную операционную систему проектов и знаний.
- В системе участвуют: My Dashboard, Obsidian/KnowledgeBase, NotebookLM, MCP, локальные агентные workflow, chat/session memory, вспомогательные скрипты и runtime-конфиги.
- Во вложениях есть:
  1) manifest с границами системы и замечаниями по чувствительным зонам;
  2) полный inventory файлов с абсолютными путями;
  3) curated archive с ключевыми файлами архитектуры, кода и knowledge-layer.

Твоя задача:
1. Восстановить карту системы:
   - основные подсистемы;
   - их роли;
   - потоки данных;
   - где сейчас source of truth;
   - где execution layer;
   - где memory/knowledge layer;
   - где UI/operational layer.
2. Выявить:
   - функциональные дублирования;
   - архитектурные конфликты;
   - слабые места в связности;
   - признаки технического долга;
   - места, где система уже зрелая и устойчивая.
3. Оценить целесообразность текущего разделения ролей между:
   - Dashboard
   - KnowledgeBase / Obsidian
   - NotebookLM
   - brain/session store
   - workflows / scripts
   - MCP / tool layer
4. Предложить целевую архитектуру развития:
   - pragmatic target state;
   - canonical source of truth;
   - launch/execution contract для агентов;
   - memory strategy;
   - data model / registry strategy;
   - write-back policy.
5. Дать roadmap:
   - short-term
   - mid-term
   - long-term
6. Отдельно дать:
   - quick wins на 1–2 недели;
   - high-leverage refactors;
   - что нельзя сейчас смешивать;
   - что пока не стоит автоматизировать;
   - что можно переводить в полуавтономный / автономный режим.
7. Если для качественного вывода не хватает содержимого конкретных файлов, запроси их ПО ИМЕННОМУ АБСОЛЮТНОМУ ПУТИ из inventory.

Формат ответа:
1. Executive summary
2. Current architecture map
3. Strengths
4. Weaknesses / risks
5. Overlap and duplication analysis
6. Recommended target architecture
7. Recommended operating model
8. Roadmap
9. Quick wins
10. Additional files requested by exact path

Важно:
- Не ограничивайся общими советами.
- Давай именно системные, реализуемые рекомендации.
- Разделяй факты, выводы и гипотезы.
- Если видишь, что отдельные подсистемы нужно слить, разделить или понизить в роли — укажи это прямо.
