def message(key, variable_1=False, variable_2=False):
    messages = {
        'email_exists': f'Email {variable_1} is already exists',
        'success_register': 'New account was registered successfully',
        'JWT_generated': 'JWT tokens were generated',
        'bad_auth_data': f'Email {variable_1} or password is wrong',
        'revoked_token': 'Access token revoked',
        'foreign_token': 'This account does not belong to you!',
        'user_not_exists': 'User not exists or password is wrong',
        'success_change_password': 'password changed successfully',
        'not_found_profile': 'Profile not exists.',
        'foreign_profile': 'This profile does not belong to you!',
        'success_change_profile': 'profile changed successfully',
        'foreign_history': 'This histories does not belong to you!',
        'access_error': 'Access error.',
        'success_delete_role': f'Role with id = {variable_1} for user with id = {variable_2} is deleted.',
        'not_found_data': f'There is no data with id = {variable_1}.',
        'obj_exists': f'{variable_1} already exists.',
        'obj_not_update': f"{variable_1} can't be updated.",
        'obj_not_role': f'{variable_1} has no roles.',
        'role_not_found': f'There is no role with name = {variable_1}',
        'request_id_required': 'request id is required'
    }
    return messages.get(key)
