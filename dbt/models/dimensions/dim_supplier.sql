with s as (
  select distinct supplier_name, supplier_city
  from {{ ref('stg_supply_chain') }}
  where supplier_name is not null
)
select
  md5(supplier_name || '_' || coalesce(supplier_city,'')) as supplier_id,
  supplier_name,
  supplier_city
from s
