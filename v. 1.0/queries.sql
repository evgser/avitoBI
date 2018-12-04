/* Промежуточный запрос: вычисление дельты между созданием тикета и ответом */
select user_id, extract (epoch from fact_reaction_dt - activity_start_dt) / 60 as delta
from support_tickets;
/* Промежуточный запрос: получение доступных оценок пользователей */
select distinct result_mentioned_by_user
from users_evaluation_of_satisfaction;


/* Часть 1 */
/* Отсортированное количество запросов по типу обращения в поддержку
   Топ категорий запросов (больше 10000 по одной тематике) */
select ticket_category, ticket_subcategory, count_tickets
from (
  select distinct ticket_category, ticket_subcategory, count(*) as count_tickets
	from support_tickets
	group by ticket_category, ticket_subcategory
	order by ticket_category ) as results
where count_tickets > 10000
order by count_tickets DESC;


/* Часть 2 */
/* Выделение данных из обращений в поддержку + пустые оценки */
select 
	user_id, 
	extract (epoch from fact_reaction_dt - activity_start_dt) / 60 as delta,
	ticket_category,
	ticket_subcategory,
	result_mentioned_by_user
from 
	support_tickets 
	left join users_evaluation_of_satisfaction 
		on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
where 
	result_mentioned_by_user not in ('Отлично','Хорошо') or 
	result_mentioned_by_user is null
order by ticket_category, ticket_subcategory;


/* Часть 2.1 */
/* Фильтр категорий на обращения в поддержку */
select 
	user_id, 
	extract (epoch from fact_reaction_dt - activity_start_dt) / 60 as delta,
	ticket_category,
	ticket_subcategory,
	result_mentioned_by_user
from 
	support_tickets 
	left join users_evaluation_of_satisfaction 
		on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
where 
	(result_mentioned_by_user not in ('Отлично','Хорошо') or 
	result_mentioned_by_user is null) and 
	concat(ticket_category, ticket_subcategory) in (
		select concat(ticket_category, ticket_subcategory)
		from (
			select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
			from support_tickets
			group by ticket_category, ticket_subcategory ) as results
		where count_tickets > 10000);


/* Часть 2.1.1 */
/* Выделение обращений в поддержку с положительными оценками и с фильтром из части 1 */
select 
	user_id, 
	extract (epoch from fact_reaction_dt - activity_start_dt) / 60 as delta,
	ticket_category,
	ticket_subcategory,
	result_mentioned_by_user
from 
	support_tickets 
	left join users_evaluation_of_satisfaction 
		on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
where 
	result_mentioned_by_user in ('Отлично','Хорошо') and 
	concat(ticket_category, ticket_subcategory) in (
		select concat(ticket_category, ticket_subcategory)
		from (
			select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
			from support_tickets
			group by ticket_category, ticket_subcategory ) as results
		where count_tickets > 10000);


/* Часть 2.1.2 */
/* Выделение обращений в поддержку с отрицательными оценками и с фильтром из части 1 */
select 
	user_id, 
	extract (epoch from fact_reaction_dt - activity_start_dt) / 60 as delta,
	ticket_category,
	ticket_subcategory,
	result_mentioned_by_user
from 
	support_tickets 
	left join users_evaluation_of_satisfaction 
		on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
where 
	result_mentioned_by_user = 'Не удовлетворительно' and 
	concat(ticket_category, ticket_subcategory) in (
		select concat(ticket_category, ticket_subcategory)
		from (
			select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
			from support_tickets
			group by ticket_category, ticket_subcategory ) as results
		where count_tickets > 10000);


/* Часть 3 */
/* Выборка пользователей и их объявлений с фильтром запросов из части 2.1 */
select 
	new_items_by_support_users.user_id,
	item_starttime,
	item_category,
	item_subcategory
from 
	new_items_by_support_users
	inner join(
		select 
			distinct user_id,
			ticket_category,
			ticket_subcategory,
			result_mentioned_by_user
		from 
			support_tickets 
			left join users_evaluation_of_satisfaction 
				on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
		where 
			(result_mentioned_by_user not in ('Отлично','Хорошо') or 
			result_mentioned_by_user is null) and 
			concat(ticket_category, ticket_subcategory) in (
				select concat(ticket_category, ticket_subcategory)
				from (
					select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
					from support_tickets
					group by ticket_category, ticket_subcategory ) as results
				where count_tickets > 10000)) as supports_category
		on new_items_by_support_users.user_id = supports_category.user_id
order by user_id;


/* Часть 3.1 */
/* Выборка пользователей и их объявлений, которые поставили положительную оценку, 
   с фильтром запросов из части 2.1 */
select 
	new_items_by_support_users.user_id,
	item_starttime,
	item_category,
	item_subcategory
from 
	new_items_by_support_users
	inner join(
		select 
			distinct user_id,
			ticket_category,
			ticket_subcategory,
			result_mentioned_by_user
		from 
			support_tickets 
			left join users_evaluation_of_satisfaction 
				on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
		where 
			result_mentioned_by_user in ('Отлично','Хорошо') and 
			concat(ticket_category, ticket_subcategory) in (
				select concat(ticket_category, ticket_subcategory)
				from (
					select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
					from support_tickets
					group by ticket_category, ticket_subcategory ) as results
				where count_tickets > 10000)) as supports_category
		on new_items_by_support_users.user_id = supports_category.user_id
order by user_id;


/* Часть 3.2 */
/* Выборка пользователей и их объявлений, которые поставили отрицательную оценку, 
   с фильтром запросов из части 2.1 */
select 
	new_items_by_support_users.user_id,
	item_starttime,
	item_category,
	item_subcategory
from 
	new_items_by_support_users
	inner join(
		select 
			distinct user_id,
			ticket_category,
			ticket_subcategory,
			result_mentioned_by_user
		from 
			support_tickets 
			left join users_evaluation_of_satisfaction 
				on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
		where 
			result_mentioned_by_user = 'Не удовлетворительно' and 
			concat(ticket_category, ticket_subcategory) in (
				select concat(ticket_category, ticket_subcategory)
				from (
					select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
					from support_tickets
					group by ticket_category, ticket_subcategory ) as results
				where count_tickets > 10000)) as supports_category
		on new_items_by_support_users.user_id = supports_category.user_id
order by user_id;