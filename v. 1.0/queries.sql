/* ������������� ������: ���������� ������ ����� ��������� ������ � ������� */
select user_id, extract (epoch from fact_reaction_dt - activity_start_dt) / 60 as delta
from support_tickets;
/* ������������� ������: ��������� ��������� ������ ������������� */
select distinct result_mentioned_by_user
from users_evaluation_of_satisfaction;


/* ����� 1 */
/* ��������������� ���������� �������� �� ���� ��������� � ���������
   ��� ��������� �������� (������ 10000 �� ����� ��������) */
select ticket_category, ticket_subcategory, count_tickets
from (
  select distinct ticket_category, ticket_subcategory, count(*) as count_tickets
	from support_tickets
	group by ticket_category, ticket_subcategory
	order by ticket_category ) as results
where count_tickets > 10000
order by count_tickets DESC;


/* ����� 2 */
/* ��������� ������ �� ��������� � ��������� + ������ ������ */
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
	result_mentioned_by_user not in ('�������','������') or 
	result_mentioned_by_user is null
order by ticket_category, ticket_subcategory;


/* ����� 2.1 */
/* ������ ��������� �� ��������� � ��������� */
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
	(result_mentioned_by_user not in ('�������','������') or 
	result_mentioned_by_user is null) and 
	concat(ticket_category, ticket_subcategory) in (
		select concat(ticket_category, ticket_subcategory)
		from (
			select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
			from support_tickets
			group by ticket_category, ticket_subcategory ) as results
		where count_tickets > 10000);


/* ����� 2.1.1 */
/* ��������� ��������� � ��������� � �������������� �������� � � �������� �� ����� 1 */
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
	result_mentioned_by_user in ('�������','������') and 
	concat(ticket_category, ticket_subcategory) in (
		select concat(ticket_category, ticket_subcategory)
		from (
			select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
			from support_tickets
			group by ticket_category, ticket_subcategory ) as results
		where count_tickets > 10000);


/* ����� 2.1.2 */
/* ��������� ��������� � ��������� � �������������� �������� � � �������� �� ����� 1 */
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
	result_mentioned_by_user = '�� �����������������' and 
	concat(ticket_category, ticket_subcategory) in (
		select concat(ticket_category, ticket_subcategory)
		from (
			select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
			from support_tickets
			group by ticket_category, ticket_subcategory ) as results
		where count_tickets > 10000);


/* ����� 3 */
/* ������� ������������� � �� ���������� � �������� �������� �� ����� 2.1 */
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
			(result_mentioned_by_user not in ('�������','������') or 
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


/* ����� 3.1 */
/* ������� ������������� � �� ����������, ������� ��������� ������������� ������, 
   � �������� �������� �� ����� 2.1 */
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
			result_mentioned_by_user in ('�������','������') and 
			concat(ticket_category, ticket_subcategory) in (
				select concat(ticket_category, ticket_subcategory)
				from (
					select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
					from support_tickets
					group by ticket_category, ticket_subcategory ) as results
				where count_tickets > 10000)) as supports_category
		on new_items_by_support_users.user_id = supports_category.user_id
order by user_id;


/* ����� 3.2 */
/* ������� ������������� � �� ����������, ������� ��������� ������������� ������, 
   � �������� �������� �� ����� 2.1 */
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
			result_mentioned_by_user = '�� �����������������' and 
			concat(ticket_category, ticket_subcategory) in (
				select concat(ticket_category, ticket_subcategory)
				from (
					select distinct ticket_category, ticket_subcategory, count(*) as count_tickets 
					from support_tickets
					group by ticket_category, ticket_subcategory ) as results
				where count_tickets > 10000)) as supports_category
		on new_items_by_support_users.user_id = supports_category.user_id
order by user_id;