from icvUI.dbsession import *


# 根据用户权限查询其能够管理的人员参数
def query_user_data(user,offset,limit,search_user):
	try:
		conn = mc.connect(**fs_icv_db)
		cursor = conn.cursor(dictionary = True)	

		result = []
		if user.role == 'superadmin': # 超级管理员
			query_sql = "SELECT user_name,user_code,role,group_name FROM ((SELECT *, substring_index(account.group_id,'-',-1) as t_gid FROM account) as temp),user_group WHERE temp.t_gid = user_group.gid AND temp.user_name LIKE '%{}%' ORDER BY case when temp.user_name = 'admin' then 0 else 1 end,temp.group_id;".format(search_user)
			cursor.execute(query_sql)
			data = cursor.fetchall()

			for single in data:
				if single['role'] == 'superadmin':
					single['user_limit'] = '报表查看;图像识别;用户管理'
					single['role'] = '超级管理员'
				elif single['role'] == 'admin':
					single['user_limit'] = '报表查看;图像识别;班组用户管理'
					single['role'] = '班组管理员'
				else:
					single['user_limit'] = '报表查看;图像识别'
					single['role'] = '普通用户'

			returndata = data[offset:offset+limit]
			result = {
					'total':len(data),
					'rows':returndata
				}

		elif user.role == 'admin': # 普通管理员
			query_sql = "SELECT user_name,user_code,role,group_name FROM account,user_group WHERE (SELECT substring(account.group_id,3) = user_group.gid AND account.group_id = '{}')  AND account.user_name LIKE '%{}%' ORDER BY account.role;".format(user.group_id,search_user)
			# print(data_sql)
			cursor.execute(query_sql)
			data = cursor.fetchall()

			for single in data:
				if single['role'] == 'admin':
					single['user_limit'] = '报表查看;图像识别;班组用户管理'
					single['role'] = '班组管理员'
				else:
					single['user_limit'] = '报表查看;图像识别'
					single['role'] = '普通用户'

			returndata = data[offset:offset+limit]
			result = {
					'total':len(data),
					'rows':returndata
				}
		else:
			pass
		return result
	except Exception as e:
		print(e)
		return None
	finally:
		cursor.close()
		conn.close()

# 查询所属组提供给前端option使用
def query_groups(user):
	try:			
		conn = mc.connect(**fs_icv_db)
		cursor = conn.cursor(dictionary = True)

		if user.role == 'superadmin':
			query_sql = "SELECT gid,group_name FROM user_group;"
			cursor.execute(query_sql)
			data = cursor.fetchall()
			cursor.close()
			conn.close()
			return data
		if user.role == 'admin':
			group_id = current_user.group_id.split('-')
			query_sql = "SELECT gid,group_name FROM user_group WHERE user_group.gid = {};".format(group_id[1])
			cursor.execute(query_sql)
			data = cursor.fetchall()
			cursor.close()
			conn.close()
			return data
		return None
	except Exception as e:
		print(e)
		return None

# 添加用户所进行的数据库操作
def insert_user(username,usercode,password,role,userfrom):
	try:
		conn = mc.connect(**fs_icv_db)
		cursor = conn.cursor()

		# 检验此用户账号是否已经注册
		search_sql = "SELECT user_code FROM account;"
		cursor.execute(search_sql)
		usercode_data = cursor.fetchall()
		if usercode in usercode_data:
			return 'wrong'

		# 只属于输电所，group_id 是 1，否则1-x
		if userfrom == '1':
			group_id = userfrom
		else:
			group_id = "1-" + userfrom

		# 插入添加的数据
		account_sql = "INSERT INTO account(group_id, user_name, user_code, role, pwd) VALUES('{}','{}','{}','{}',PASSWORD('{}'));".format(group_id,username,usercode,role,password)
		
		cursor.execute(account_sql)
		conn.commit()
		return 'right'
	except Exception as e:
		print(e)
		return 'wrong'
	finally:
		cursor.close()
		conn.close()

# 修改用户
def update_user(username,usercode,role,userfrom):
	try:
		conn = mc.connect(**fs_icv_db)
		cursor = conn.cursor(dictionary=True)

		if userfrom == '1':
			group_id = '1'
		else:
			group_id = '1-' + userfrom

		update_sql = "UPDATE account SET role = '{}',group_id = '{}' WHERE user_code = '{}' AND user_name = '{}';".format(role,group_id,usercode,username)
		cursor.execute(update_sql)
		conn.commit()
		cursor.close()
		conn.close()
		return 'right'	
	except Exception as e:
		print(e)
		return 'wrong'

# 删除用户
def delete_user(del_data):
	try:
		conn = mc.connect(**fs_icv_db)
		cursor = conn.cursor(dictionary=True)

		if len(del_data.split(',')) == 1:
			del_sql = "DELETE FROM account WHERE user_code = '{}';".format(del_data)
		else:
			del_data = tuple(del_data.split(','))
			del_sql = "DELETE FROM account WHERE user_code IN {};".format(del_data)
		cursor.execute(del_sql)
		conn.commit()
		cursor.close()
		conn.close()
		return 'right'
	except Exception as e:
		print(e)
		return 'wrong'

# 修改密码
def update_password(mod_user,mod_pwd):
	try:
		conn = mc.connect(**fs_icv_db)
		cursor = conn.cursor(dictionary=True)
		mod_pwd_sql = "UPDATE account SET pwd = (PASSWORD('{}')) WHERE user_code = '{}';".format(mod_pwd,mod_user)
		cursor.execute(mod_pwd_sql)
		conn.commit()
		cursor.close()
		conn.close()
		return 'right'
	except Exception as e:
		print(e)
		return 'wrong'
