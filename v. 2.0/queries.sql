/* Промежуточные обращения */
/* Подсчёт количества обращений в поддержку на каждого пользователя */
select
	distinct user_id,
	count(*) as count_tickets
from
	support_tickets
group by user_id;


/* Подсчёт количества пользователей с 1 обращением */
select count(*) as count_i
from(
	select user_id, count_tickets
	from(
		select
			distinct user_id,
			count(*) as count_tickets
		from
			support_tickets
		group by user_id) as tab
	where count_tickets = 1
	order by user_id) as new_tab;

/* Подсчёт пользователей с любым количеством обращений */
select count(*) as all_count
from(
	select
		distinct user_id,
		count(*) as count_tickets
	from
		support_tickets
	group by user_id) as tab;
	
	
	
/* 1 часть: расчёт критерия эффективности службы поддержки */
/* [2.0.0] выборка из поддержки с 1 обращением */
select
	distinct user_id,
	activity_start_dt,
	result_mentioned_by_user
from
	support_tickets
	inner join users_evaluation_of_satisfaction
		on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
where 
	user_id in (
		select 
			user_id
		from(
			select
				distinct user_id,
				count(*) as count_tickets
			from
				support_tickets
			group by user_id) as uniq_users_tab
		where count_tickets = 1) 
	and 
	user_id in (
		select
			distinct user_id
		from
			new_items_by_support_users) 
order by user_id;


/* [2.0.1] выборка из поддержки с 1 обращением с категориями */
select
	distinct user_id,
	activity_start_dt,
	ticket_category,
	ticket_subcategory,
	result_mentioned_by_user
from
	support_tickets
	inner join users_evaluation_of_satisfaction
		on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
where 
	user_id in (
		select 
			user_id
		from(
			select
				distinct user_id,
				count(*) as count_tickets
			from
				support_tickets
			group by user_id) as uniq_users_tab
		where count_tickets = 1) 
	and 
	user_id in (
		select
			distinct user_id
		from
			new_items_by_support_users) 
order by user_id;


/* [3.0.0] выборка объявлений пользователей с 1 обращением */ 
select
	user_id,
	item_starttime
from
	new_items_by_support_users
where
	user_id in (
		select
			distinct user_id
		from
			support_tickets
			inner join users_evaluation_of_satisfaction
				on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
		where user_id in (
			select 
				user_id
			from(
				select
					distinct user_id,
					count(*) as count_tickets
				from
					support_tickets
				group by user_id) as uniq_users_tab
			where count_tickets = 1))
order by user_id;

/* 2 часть: подсчёт урона Авито */
/*  */



