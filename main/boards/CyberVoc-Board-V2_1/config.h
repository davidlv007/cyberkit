#ifndef _BOARD_CONFIG_H_
#define _BOARD_CONFIG_H_

#include <driver/gpio.h>
#include <driver/uart.h>
#include <driver/spi_master.h>

// CyberVoc-Board-V2_1 pin mapping (ported from vocat-3 cyber-vocat)

#define AUDIO_INPUT_SAMPLE_RATE  24000
#define AUDIO_OUTPUT_SAMPLE_RATE 24000
#define AUDIO_INPUT_REFERENCE    true

/*
 * 仅软件关机（无软件开机，上电由硬件完成）：
 * - PG1(GPIO40) 关机键输入：按下为高，松开为低；长按触发关机提示
 * - PG2(GPIO38) 关机控制输出：上电保持低；高电平 100–300ms 脉冲断电
 */
#define PG1_POWER_KEY_GPIO          GPIO_NUM_40
#define PG1_POWER_KEY_ACTIVE_LEVEL  1
#define PG2_HOLD_GPIO               GPIO_NUM_38
#define PG2_HOLD_ACTIVE_LEVEL       1
#define PG2_POWER_OFF_PULSE_MS      200

/*
 * 长按 1.5s → 关机提示 → 提示结束再发 PG2。
 * 开机：必须先检测到松开，忽略窗口后再要求一次「空闲松开」，
 * 避免上电按住过久、忽略窗口结束时仍按着被当成关机长按。
 */
#define KEY_SW1_LONG_PRESS_MS       1500
#define KEY_SHUTDOWN_HINT_HOLD_MS   2500
#define KEY_GPIO_POLL_MS            50
#define KEY_ARM_RELEASE_STABLE_MS   400
#define KEY_POST_ARM_IGNORE_MS      3000
#define KEY_PRESS_STABLE_MS         100
#define KEY_RELEASE_RESET_MS        250

#define AUDIO_I2S_GPIO_MCLK     GPIO_NUM_5
#define AUDIO_I2S_GPIO_WS       GPIO_NUM_7
#define AUDIO_I2S_GPIO_BCLK     GPIO_NUM_15
#define AUDIO_I2S_GPIO_DIN      GPIO_NUM_16
#define AUDIO_I2S_GPIO_DOUT     GPIO_NUM_6

#define AUDIO_CODEC_PA_PIN      GPIO_NUM_4
#define AUDIO_CODEC_I2C_SDA_PIN  GPIO_NUM_2
#define AUDIO_CODEC_I2C_SCL_PIN  GPIO_NUM_1
#define AUDIO_CODEC_ES8311_ADDR  ES8311_CODEC_DEFAULT_ADDR
#define AUDIO_CODEC_ES7210_ADDR  ES7210_CODEC_DEFAULT_ADDR

/* QMA6100P shares the codec I2C bus (SDA/SCL above). */
#define QMA6100P_I2C_ADDR       0x12

#define BOOT_BUTTON_GPIO        GPIO_NUM_0

#define DISPLAY_WIDTH       360
#define DISPLAY_HEIGHT      360
#define DISPLAY_MIRROR_X    false
#define DISPLAY_MIRROR_Y    false
#define DISPLAY_SWAP_XY     false

#define QSPI_LCD_H_RES           (360)
#define QSPI_LCD_V_RES           (360)
#define QSPI_LCD_BIT_PER_PIXEL   (16)

#define QSPI_LCD_HOST           SPI2_HOST
#define QSPI_PIN_NUM_LCD_PCLK   GPIO_NUM_21
#define QSPI_PIN_NUM_LCD_CS     GPIO_NUM_10
#define QSPI_PIN_NUM_LCD_DATA0  GPIO_NUM_14
#define QSPI_PIN_NUM_LCD_DATA1  GPIO_NUM_9
#define QSPI_PIN_NUM_LCD_DATA2  GPIO_NUM_13
#define QSPI_PIN_NUM_LCD_DATA3  GPIO_NUM_46
#define QSPI_PIN_NUM_LCD_RST    GPIO_NUM_47
#define QSPI_PIN_NUM_LCD_TE     GPIO_NUM_12
#define QSPI_PIN_NUM_LCD_BL     GPIO_NUM_3

#define UART1_TX     GPIO_NUM_41
#define UART1_RX     GPIO_NUM_42

#define TOUCH_PAD2     GPIO_NUM_20
#define TOUCH_PAD1     GPIO_NUM_NC
#define HEAD_TOUCH_GPIO          TOUCH_PAD2
#define HEAD_TOUCH_ACTIVE_LEVEL  1

#define SPEAKING_LED_GPIO          GPIO_NUM_19
#define SPEAKING_LED_ACTIVE_LEVEL  0

#define DISPLAY_OFFSET_X  0
#define DISPLAY_OFFSET_Y  0

#define TP_PORT          (I2C_NUM_0)
#define TP_PIN_NUM_RST   (GPIO_NUM_NC)
#define TP_PIN_NUM_INT   (GPIO_NUM_11)

#define DISPLAY_BACKLIGHT_PIN           QSPI_PIN_NUM_LCD_BL
#define DISPLAY_BACKLIGHT_OUTPUT_INVERT false

#define LCD_CORE PRO_CPU_NUM

#define TAIJIPI_ST77916_PANEL_BUS_QSPI_CONFIG(sclk, d0, d1, d2, d3, max_trans_sz,cpu) \
    {                                                                             \
        .data0_io_num = d0,                                                       \
        .data1_io_num = d1,                                                       \
        .sclk_io_num = sclk,                                                      \
        .data2_io_num = d2,                                                       \
        .data3_io_num = d3,                                                       \
        .max_transfer_sz = max_trans_sz,                                          \
        .isr_cpu_id = cpu,                                                        \
    }

// SD card（PG2 已换到 GPIO38，故 D0 可用 GPIO39）
#define BSP_SD_CLK          GPIO_NUM_48
#define BSP_SD_CMD          GPIO_NUM_45
#define BSP_SD_D0           GPIO_NUM_39
#define MOUNT_POINT         "/sdcard"

// ML307 4G module (high level = enabled)
#define ML307_RX_PIN            GPIO_NUM_18
#define ML307_TX_PIN            GPIO_NUM_8
#define ML307_UART_NUM          UART_NUM_2
#define ML307_EN_PIN            GPIO_NUM_17

#endif // _BOARD_CONFIG_H_
