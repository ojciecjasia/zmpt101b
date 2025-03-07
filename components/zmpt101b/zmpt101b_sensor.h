#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "zmpt101b.h"

static const char *const TAG = "zmpt101b";

namespace esphome
{
  namespace zmpt101b
  {

    class ZMPT101BSensor : public sensor::Sensor, public PollingComponent
    {
    public:
      float get_setup_priority() const override { return setup_priority::DATA; };
      void set_pin(InternalGPIOPin *pin) { this->pin_ = pin; }
      void set_frequency(float frequency) { this->frequency_ = frequency; }
      void set_sensitivity(float sensitivity) { this->sensitivity_ = sensitivity; }

      void update() override
      {
        float voltage = this->voltageSensor_->getRmsVoltage();
        this->publish_state(voltage);
      }

      /// Set up the internal sensor array.
      void setup() override
      {
        ESP_LOGCONFIG(TAG, "Setting up ZMPT101B...");

        this->pin_->setup();

        this->voltageSensor_ = new ZMPT101B(this->pin_->get_pin(), this->frequency_, this->sensitivity_);
      };
      void dump_config() override {
        ESP_LOGCONFIG(TAG, "ZMPT101B");
        LOG_PIN("Pin: ", this->pin_);
        ESP_LOGCONFIG(TAG, "Frequency: %2f", this->frequency_);
        ESP_LOGCONFIG(TAG, "Sensitivity: %2f", this->sensitivity_);
      };

    protected:
      ZMPT101B *voltageSensor_;

    private:
      InternalGPIOPin *pin_;
      float frequency_;
      float sensitivity_;
    };

  } // namespace zmpt101b
} // namespace esphome
