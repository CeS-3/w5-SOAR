# 智能决策部分提供的 API 文档

> 本文档描述了与智能决策部分相关的三个主要API动作，包括事件信息传递、响应策略建议和事件状态更新。

## 事件信息传递 API

### 功能描述

此 API 用于发送获取到的安全事件信息，以便进行进一步的处理和存储。

### API 详情

- **Endpoint:** `/api/events/send`
- **Method:** POST
- **Required Parameters:**
  - `event_info` (JSON object): 包含事件的详细信息。

### 返回值

- **Success:** 返回`{"status": 0, "message": "Event information sent successfully"}`
- **Failure:** 返回`{"status": 2, "message": "请求事件信息传递API失败"}` 或具体错误信息

## 响应策略建议 API

### 功能描述

根据事件ID, 获取对该事件的响应策略建议。

### API 详情

- **Endpoint:** `/api/decision/response_suggestions`
- **Method:** GET
- **Query Parameters:**
  - `event_id` (string): 事件的唯一标识符。

### 返回值

- **Success:** 返回包含建议列表的`{"status": 0, "suggestions": [...]}` 
- **Failure:** 返回`{"status": 2, "message": "获取响应策略建议失败"}` 或具体错误信息

## 事件状态更新 API

### 功能描述

通过提供事件ID和新状态，更新安全事件的状态。

### API 详情

- **Endpoint:** `/api/events/update_status`
- **Method:** POST
- **Request Body:**
  - `event_id` (string): 事件的唯一标识符。
  - `new_status` (string): 新的状态描述。

### 返回值

- **Success:** 返回`{"status": 0, "message": "Event status updated successfully"}`
- **Failure:** 返回`{"status": 2, "message": "更新事件状态失败"}` 或具体错误信息

