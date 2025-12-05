with sales as (
  select product_id, sum(quantity_sold) as total_sold, sum(revenue) as total_revenue
  from {{ ref('fact_sales') }}
  group by product_id
),
manufacturing as (
  select product_id, avg(defect_rate) as avg_defect_rate, avg(mfg_lead_time_days) as avg_mfg_lead_time
  from {{ ref('stg_supply_chain') }}
  group by product_id
)
select
  s.product_id,
  s.total_sold,
  s.total_revenue,
  m.avg_defect_rate,
  m.avg_mfg_lead_time
from sales s
left join manufacturing m using (product_id)
