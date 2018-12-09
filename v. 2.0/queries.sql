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
/* [2.1.0] выборка всех обращенией из поддержки без оценки*/
select
	distinct user_id,
	activity_start_dt,
	ticket_category,
	ticket_subcategory
from
	support_tickets
where
	user_id in (
		select
			distinct user_id
		from
			new_items_by_support_users) 
order by user_id;


/* [2.1.1] выборка из поддержки с 1 обращением без оценки */
select
	distinct user_id,
	activity_start_dt,
	ticket_category,
	ticket_subcategory
from
	support_tickets
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


/* [3.1.0] выборка всех объявлений пользователей  */
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
			support_tickets)
order by user_id;


/* [3.1.1] выборка объявлений пользователей с 1 обращением */
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



/* Промежуточные обращения */
/* Количество всех пользователей с обращениями в поддержку 1 раз (с и без оценки) */
select count(*) as count_tikcets_without_rate_1
from(
	select user_id, count_tickets
	from(
		select
			distinct user_id,
			count(*) as count_tickets
		from
			support_tickets
		where
			user_id in (
				select 
					distinct user_id
				from
					new_items_by_support_users)
		group by user_id) as tab
	where count_tickets = 1
	order by user_id) as new_tab;

/* Количество всех пользователей с обращениями в поддержку (с и без оценки) */
select count (*) as count_tickets_without_rate
from (
	select 
		distinct user_id
	from 
		new_items_by_support_users
	where user_id in(
		select
			distinct user_id
		from
			support_tickets)) as new_tab;

/* Количество обращений в поддержку 1 раз (с оценкой) */
select count (*) as count_tickets_with_rate_1
from(
	select distinct user_id
	from 
		support_tickets
		inner join users_evaluation_of_satisfaction
		on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
	where user_id in (
		select 
			distinct user_id
		from 
			new_items_by_support_users)
	and user_id in (
		select user_id
		from(
			select 
				user_id, count_tickets
			from(
				select
					distinct user_id,
					count(*) as count_tickets
				from
					support_tickets
				group by user_id) as tab
			where count_tickets = 1) as new_tab
		order by user_id)) as new_new_tab;

/* Количество всех обращений в поддержку (с оценкой) */
select count (*) as count_tickets_with_rate
from(
	select distinct user_id
	from 
		support_tickets
		inner join users_evaluation_of_satisfaction
		on support_tickets.request_id = users_evaluation_of_satisfaction.request_id
	where user_id in (
		select 
			distinct user_id
		from 
			new_items_by_support_users)
	order by user_id) as tab;
