import pytest
import os
import time
from logperformance import LogPerformance
from unittest.mock import patch


class TestLogPerformance:
    @pytest.fixture
    def logger(self):
        return LogPerformance()

    def test_singleton_pattern(self):
        logger1 = LogPerformance()
        logger2 = LogPerformance()
        assert logger1 is logger2

    def test_check_exists_directory(self, logger, tmp_path):
        # Test existing directory
        assert logger.check_exists_directory(str(tmp_path)) is True

        # Test non-existing directory
        non_existent_dir = os.path.join(str(tmp_path), "nonexistent")
        assert logger.check_exists_directory(non_existent_dir) is False

    def test_create_directory(self, logger, tmp_path):
        new_dir = os.path.join(str(tmp_path), "new_dir")
        logger.create_directory(new_dir)
        assert os.path.exists(new_dir)

    def test_log_performance(self, logger):
        @logger.log_performance
        def test_func():
            time.sleep(0.1)
            return "test"

        with patch.object(logger.logger, "debug") as mock_debug:
            result = test_func()
            assert result == "test"
            mock_debug.assert_called_once()

    def test_log_error(self, logger):
        @logger.log_error
        def error_func():
            raise ValueError("Test error")

        with patch.object(logger.logger, "error") as mock_error:
            with pytest.raises(ValueError):
                error_func()
            mock_error.assert_called_once()

    def test_log_warning(self, logger):
        @logger.log_warning
        def warning_func():
            time.sleep(0.1)
            return "test"

        with patch.object(logger, "warning") as mock_warning:
            result = warning_func()
            assert result == "test"
            mock_warning.assert_called_once()

    def test_info(self, logger):
        with patch.object(logger.logger, "info") as mock_info:
            logger.info("Test info message")
            mock_info.assert_called_once()

    def test_warning(self, logger):
        with patch.object(logger.logger, "warning") as mock_warning:
            logger.warning("Test warning message")
            mock_warning.assert_called_once()

    def test_error(self, logger):
        with patch.object(logger.logger, "error") as mock_error:
            logger.error("Test error message")
            mock_error.assert_called_once()

    def test_append_log_message(self, logger):
        test_msg = "Test message"
        logger._append_log_message(test_msg, 20)  # 20 is logging.INFO
        assert logger.log_messages == test_msg

    def test_environment_variables(self, logger):
        with patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}):
            logger = LogPerformance()
            assert logger.logger.level == 20  # logging.DEBUG

        with patch.dict(os.environ, {"DEBUG_WRITE_FILE": "False"}):
            logger = LogPerformance()
            assert logger._instance
            assert logger.initialized
