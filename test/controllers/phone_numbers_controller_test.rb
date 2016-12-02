require 'test_helper'

class PhoneNumbersControllerTest < ActionDispatch::IntegrationTest
  setup do
    @phone_number = phone_numbers(:one)
  end

  test "should get index" do
    get phone_numbers_url
    assert_response :success
  end

  test "should get new" do
    get new_phone_number_url
    assert_response :success
  end

  test "should create phone_number" do
    assert_difference('PhoneNumber.count') do
      post phone_numbers_url, params: { phone_number: { active: @phone_number.active, phone_number: @phone_number.phone_number } }
    end

    assert_redirected_to phone_number_url(PhoneNumber.last)
  end

  test "should show phone_number" do
    get phone_number_url(@phone_number)
    assert_response :success
  end

  test "should get edit" do
    get edit_phone_number_url(@phone_number)
    assert_response :success
  end

  test "should update phone_number" do
    patch phone_number_url(@phone_number), params: { phone_number: { active: @phone_number.active, phone_number: @phone_number.phone_number } }
    assert_redirected_to phone_number_url(@phone_number)
  end

  test "should destroy phone_number" do
    assert_difference('PhoneNumber.count', -1) do
      delete phone_number_url(@phone_number)
    end

    assert_redirected_to phone_numbers_url
  end
end
