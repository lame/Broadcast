require 'test_helper'

class MessagesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @message = messages(:one)
  end

  test "should get index" do
    get messages_url
    assert_response :success
  end

  test "should get new" do
    get new_message_url
    assert_response :success
  end

  test "should create message" do
    assert_difference('Message.count') do
      post messages_url, params: { message: { body: @message.body, from_country: @message.from_country, from_number: @message.from_number, from_zip: @message.from_zip, id: @message.id, message_sid: @message.message_sid, status: @message.status, to_country: @message.to_country, to_number: @message.to_number, to_zip: @message.to_zip } }
    end

    assert_redirected_to message_url(Message.last)
  end

  test "should show message" do
    get message_url(@message)
    assert_response :success
  end

  test "should get edit" do
    get edit_message_url(@message)
    assert_response :success
  end

  test "should update message" do
    patch message_url(@message), params: { message: { body: @message.body, from_country: @message.from_country, from_number: @message.from_number, from_zip: @message.from_zip, id: @message.id, message_sid: @message.message_sid, status: @message.status, to_country: @message.to_country, to_number: @message.to_number, to_zip: @message.to_zip } }
    assert_redirected_to message_url(@message)
  end

  test "should destroy message" do
    assert_difference('Message.count', -1) do
      delete message_url(@message)
    end

    assert_redirected_to messages_url
  end
end
