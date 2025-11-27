import React from 'react';
import { Button } from 'antd';
import { createStyles } from 'antd-style';
import { AntDesignOutlined } from '@ant-design/icons';

interface GradientButtonProps extends React.ComponentProps<typeof Button> {
    text?: React.ReactNode; // 按钮文字
    icon?: React.ReactNode; // 可选图标
}

/**
 * GradientButton - 基于 AntD Button 的线性渐变按钮
 * 支持 text、icon、onClick、disabled、size、type 等
 */
const GradientButton: React.FC<GradientButtonProps> = ({ text, icon, children, ...props }) => {
    const { styles } = useStyle();

    return (
        <Button className={styles.linearGradientButton} icon={icon} {...props}>
            {text || children}
        </Button>
    );
};

// 使用 createStyles 定义渐变效果
const useStyle = createStyles(({ prefixCls, css }) => ({
    linearGradientButton: css`
    &.${prefixCls}-btn-primary:not([disabled]):not(.${prefixCls}-btn-dangerous) {
      position: relative;
      overflow: hidden;

      > span {
        position: relative;
        z-index: 1;
      }

      &::before {
        content: '';
        background: linear-gradient(135deg, #6253e1, #04befe);
        position: absolute;
        inset: 0;
        border-radius: inherit;
        transition: opacity 0.3s;
        opacity: 1;
        z-index: 0;
      }

      &:hover::before {
        opacity: 0.8;
      }
    }
  `,
}));

export default GradientButton;