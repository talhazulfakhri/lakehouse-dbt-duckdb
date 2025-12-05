{% macro debug_duckdb() %}
  {% set results = run_query('SELECT COUNT(*) AS cnt FROM main.raw_supply_chain') %}
  {% if results is none %}
    {{ exceptions.raise_compiler_error('run_query returned no results (possible runtime error).') }}
  {% else %}
    {{ log('COLUMNS: ' ~ results.columns | string, info=True) }}
    {{ log('ROWS: ' ~ results.rows[:5] | string, info=True) }}
  {% endif %}
{% endmacro %}
