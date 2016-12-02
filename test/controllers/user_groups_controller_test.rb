require 'test_helper'

class UserGroupsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @user_group = user_groups(:one)
  end

  test "should get index" do
    get user_groups_url
    assert_response :success
  end

  test "should get new" do
    get new_user_group_url
    assert_response :success
  end

  test "should create user_group" do
    assert_difference('UserGroup.count') do
      post user_groups_url, params: { user_group: { active: @user_group.active, user_group_name: @user_group.user_group_name } }
    end

    assert_redirected_to user_group_url(UserGroup.last)
  end

  test "should show user_group" do
    get user_group_url(@user_group)
    assert_response :success
  end

  test "should get edit" do
    get edit_user_group_url(@user_group)
    assert_response :success
  end

  test "should update user_group" do
    patch user_group_url(@user_group), params: { user_group: { active: @user_group.active, user_group_name: @user_group.user_group_name } }
    assert_redirected_to user_group_url(@user_group)
  end

  test "should destroy user_group" do
    assert_difference('UserGroup.count', -1) do
      delete user_group_url(@user_group)
    end

    assert_redirected_to user_groups_url
  end
end
