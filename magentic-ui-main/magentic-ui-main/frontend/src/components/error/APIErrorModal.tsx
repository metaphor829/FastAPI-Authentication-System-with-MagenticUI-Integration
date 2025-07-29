import React from 'react';
import { Modal, Button, Alert, Space, Typography, Divider, Card } from 'antd';
import { 
  ExclamationCircleOutlined, 
  SettingOutlined, 
  ReloadOutlined,
  CreditCardOutlined,
  ClockCircleOutlined,
  LinkOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

interface Solution {
  title: string;
  description: string;
  action: string;
  url?: string;
  models?: string[];
  primary: boolean;
}

interface APIErrorInfo {
  error_type: string;
  title: string;
  message: string;
  solutions: Solution[];
  original_error: string;
  status_code?: number;
  timestamp?: string;
}

interface APIErrorModalProps {
  visible: boolean;
  errorInfo: APIErrorInfo | null;
  onClose: () => void;
  onOpenSettings?: () => void;
  onRetry?: () => void;
  onSwitchModel?: (model: string) => void;
}

const APIErrorModal: React.FC<APIErrorModalProps> = ({
  visible,
  errorInfo,
  onClose,
  onOpenSettings,
  onRetry,
  onSwitchModel
}) => {
  if (!errorInfo) return null;

  const getErrorIcon = (errorType: string) => {
    switch (errorType) {
      case 'insufficient_credits':
        return <CreditCardOutlined style={{ color: '#ff4d4f', fontSize: '24px' }} />;
      case 'invalid_api_key':
        return <ExclamationCircleOutlined style={{ color: '#ff4d4f', fontSize: '24px' }} />;
      case 'rate_limit':
        return <ClockCircleOutlined style={{ color: '#faad14', fontSize: '24px' }} />;
      default:
        return <ExclamationCircleOutlined style={{ color: '#ff4d4f', fontSize: '24px' }} />;
    }
  };

  const getAlertType = (errorType: string) => {
    switch (errorType) {
      case 'insufficient_credits':
      case 'quota_exceeded':
        return 'warning';
      case 'invalid_api_key':
        return 'error';
      case 'rate_limit':
        return 'info';
      default:
        return 'error';
    }
  };

  const handleSolutionAction = (solution: Solution) => {
    switch (solution.action) {
      case 'open_url':
        if (solution.url) {
          window.open(solution.url, '_blank');
        }
        break;
      case 'open_settings':
        if (onOpenSettings) {
          onOpenSettings();
          onClose();
        }
        break;
      case 'retry':
      case 'retry_later':
        if (onRetry) {
          onRetry();
          onClose();
        }
        break;
      case 'suggest_models':
        // 这里可以显示模型选择器
        break;
      default:
        break;
    }
  };

  const getSolutionIcon = (action: string) => {
    switch (action) {
      case 'open_url':
        return <LinkOutlined />;
      case 'open_settings':
        return <SettingOutlined />;
      case 'retry':
      case 'retry_later':
        return <ReloadOutlined />;
      case 'suggest_models':
        return <SettingOutlined />;
      default:
        return <SettingOutlined />;
    }
  };

  return (
    <Modal
      title={
        <Space>
          {getErrorIcon(errorInfo.error_type)}
          <span>API调用失败</span>
        </Space>
      }
      open={visible}
      onCancel={onClose}
      footer={null}
      width={600}
      centered
    >
      <div style={{ padding: '16px 0' }}>
        {/* 主要错误信息 */}
        <Alert
          message={errorInfo.title}
          description={errorInfo.message}
          type={getAlertType(errorInfo.error_type)}
          showIcon
          style={{ marginBottom: '24px' }}
        />

        {/* 解决方案 */}
        <Title level={4}>💡 解决方案</Title>
        <Space direction="vertical" style={{ width: '100%' }} size="middle">
          {errorInfo.solutions.map((solution, index) => (
            <Card
              key={index}
              size="small"
              hoverable
              style={{
                border: solution.primary ? '2px solid #1890ff' : '1px solid #d9d9d9',
                backgroundColor: solution.primary ? '#f6ffed' : '#fafafa'
              }}
              onClick={() => handleSolutionAction(solution)}
            >
              <Space>
                {getSolutionIcon(solution.action)}
                <div>
                  <Text strong>{solution.title}</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    {solution.description}
                  </Text>
                </div>
              </Space>
              {solution.primary && (
                <div style={{ float: 'right' }}>
                  <Text type="success" style={{ fontSize: '12px' }}>推荐</Text>
                </div>
              )}
            </Card>
          ))}
        </Space>

        {/* 特殊处理：显示可用的免费模型 */}
        {errorInfo.error_type === 'insufficient_credits' && (
          <>
            <Divider />
            <Title level={5}>🆓 可尝试的免费模型</Title>
            <Space wrap>
              {[
                'meta-llama/llama-3.2-3b-instruct:free',
                'microsoft/phi-3-mini-128k-instruct:free',
                'google/gemma-2-9b-it:free'
              ].map(model => (
                <Button
                  key={model}
                  size="small"
                  type="dashed"
                  onClick={() => {
                    if (onSwitchModel) {
                      onSwitchModel(model);
                      onClose();
                    }
                  }}
                >
                  {model.split('/')[1]?.split(':')[0] || model}
                </Button>
              ))}
            </Space>
          </>
        )}

        {/* 技术详情（可折叠） */}
        <Divider />
        <details style={{ marginTop: '16px' }}>
          <summary style={{ cursor: 'pointer', color: '#666' }}>
            <Text type="secondary">查看技术详情</Text>
          </summary>
          <div style={{ marginTop: '8px', padding: '8px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
            <Text code style={{ fontSize: '11px', wordBreak: 'break-all' }}>
              {errorInfo.original_error}
            </Text>
            {errorInfo.status_code && (
              <div style={{ marginTop: '4px' }}>
                <Text type="secondary" style={{ fontSize: '11px' }}>
                  HTTP状态码: {errorInfo.status_code}
                </Text>
              </div>
            )}
          </div>
        </details>

        {/* 底部按钮 */}
        <div style={{ marginTop: '24px', textAlign: 'right' }}>
          <Space>
            <Button onClick={onClose}>
              关闭
            </Button>
            {onRetry && (
              <Button type="primary" icon={<ReloadOutlined />} onClick={() => {
                onRetry();
                onClose();
              }}>
                重试
              </Button>
            )}
          </Space>
        </div>
      </div>
    </Modal>
  );
};

export default APIErrorModal;
