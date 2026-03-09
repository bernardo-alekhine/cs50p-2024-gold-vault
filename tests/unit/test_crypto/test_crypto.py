import argparse
import pytest
from typing import Any, Dict, Generator
from unittest.mock import patch, MagicMock
from gvault.crypto import Crypto  # type: ignore
from gvault.crypto.utils import LinkProcessor  # type: ignore


@pytest.fixture
def mock_parse_args(mocker: Generator) -> Generator[Any, Any, None]:
    mock_parse_args: Any = mocker.Mock(spec=argparse.Namespace)  # type: ignore
    mock_parse_args.input_paths = []
    mock_parse_args.output_paths = []
    yield mock_parse_args


class TestCrypto:
    def test_crypto_init(self, mock_parse_args: Any) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        assert crypto.parse_args == mock_parse_args
        assert isinstance(crypto.link_processor, LinkProcessor)

    @patch.object(Crypto, "_get_path_type")
    @patch.object(Crypto, "_should_write_output_path")
    @patch.object(Crypto, "_process_file")
    def test_process_path_file(
        self,
        mock_process_file: MagicMock,
        mock_should_write: MagicMock,
        mock_get_path_type: MagicMock,
        mock_parse_args: MagicMock,
    ) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        mock_get_path_type.return_value = "file"
        mock_should_write.return_value = True
        crypto._process_path("input_path", "output_path")
        mock_process_file.assert_called_once_with("input_path", "output_path")

    @patch.object(Crypto, "_get_password")
    @patch.object(Crypto, "_get_path_type")
    @patch.object(Crypto, "_should_write_output_path")
    @patch.object(Crypto, "_process_dir")
    def test_process_path_directory(
        self,
        mock_process_dir: MagicMock,
        mock_should_write: MagicMock,
        mock_get_path_type: MagicMock,
        mock_get_password: MagicMock,
        mock_parse_args: MagicMock,
    ) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        mock_get_password.retrun_value = "password"
        mock_get_path_type.return_value = "directory"
        mock_should_write.return_value = True
        crypto._process_path("input_path", "output_path")
        mock_process_dir.assert_called_once_with("input_path", "output_path")

    @patch.object(Crypto, "_get_path_type")
    @patch.object(Crypto, "_should_write_output_path")
    def test_process_path_symlink(
        self, mock_should_write: MagicMock, mock_get_path_type: MagicMock, mock_parse_args: MagicMock
    ) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        mock_get_path_type.return_value = ["symlink", "file"]
        mock_should_write.return_value = True
        assert crypto._process_path("input_path", "output_path") == None

    @patch.object(Crypto, "_get_path_type")
    @patch.object(Crypto, "_should_write_output_path")
    def test_process_path_unknown(
        self, mock_should_write: MagicMock, mock_get_path_type: MagicMock, mock_parse_args: MagicMock
    ) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        mock_get_path_type.return_value = "unknown"
        mock_should_write.return_value = True
        with patch.object(crypto, "_process_file") as mock_process_file, patch.object(
            crypto, "_process_dir"
        ) as mock_process_dir:
            crypto._process_path("input_path", "output_path")
            mock_process_file.assert_not_called()
            mock_process_dir.assert_not_called()

    @patch.object(Crypto, "_get_path_type")
    @patch.object(Crypto, "_should_write_output_path")
    def test_process_path_should_not_write(self, mock_should_write: MagicMock, mock_get_path_type: MagicMock) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        mock_get_path_type.return_value = "file"
        mock_should_write.return_value = False
        with patch.object(crypto, "_process_file") as mock_process_file:
            crypto._process_path("input_path", "output_path")
            mock_process_file.assert_not_called()

    def test_process_file_encrypt(self, mock_parse_args: MagicMock) -> None:
        mock_parse_args.encrypt = True
        mock_parse_args.decrypt = False
        crypto: Crypto = Crypto(mock_parse_args)
        with patch.object(crypto, "_encrypt_file") as mock_encrypt_file, patch.object(
            crypto, "_get_password", return_value="password"
        ):
            crypto._process_file("input_file", "output_file")
            mock_encrypt_file.assert_called_once_with("input_file", "output_file")

    def test_process_file_decrypt(self, mock_parse_args: MagicMock) -> None:
        mock_parse_args.encrypt = False
        mock_parse_args.decrypt = True
        crypto: Crypto = Crypto(mock_parse_args)
        with patch.object(crypto, "_decrypt_file") as mock_decrypt_file, patch.object(
            crypto, "_get_password", return_value="password"
        ):
            crypto._process_file("input_file", "output_file")
            mock_decrypt_file.assert_called_once_with("input_file", "output_file")

    def test_get_password(self, mock_parse_args: MagicMock) -> None:
        password: str = "password"
        crypto: Crypto = Crypto(mock_parse_args)
        with patch.object(crypto, "_get_password", return_value=password):
            get_password: str = crypto._get_password()
            assert get_password == password

    @pytest.mark.parametrize(
        "path_type, expected",
        [
            ({"isfile": True, "islink": False, "isdir": False}, "file"),
            ({"isfile": False, "islink": True, "isdir": False}, "symlink"),
            ({"isfile": False, "islink": False, "isdir": True}, "directory"),
            ({"isfile": False, "islink": False, "isdir": False}, "unknown"),
        ],
    )
    def test_get_path_type(self, path_type: Dict[str, bool], expected: str, mock_parse_args: MagicMock) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        with patch("os.path.isfile") as mock_isfile, patch("os.path.islink") as mock_islink, patch(
            "os.path.isdir"
        ) as mock_isdir:
            mock_isfile.return_value = path_type["isfile"]
            mock_islink.return_value = path_type["islink"]
            mock_isdir.return_value = path_type["isdir"]
            get_path_type: str = crypto._get_path_type("dummy/path")
            assert get_path_type == expected

    def test_should_write_output(self, mock_parse_args: MagicMock) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        with patch("os.path.exists"), patch.object(crypto, "_confirm_overwrite_path") as mock_confirm_overwrite_path:
            should_write_output: bool = crypto._should_write_output_path("dummy/path")
            mock_confirm_overwrite_path.assert_called_once_with("dummy/path")
            assert should_write_output

    def test_make_output_dir(self, mock_parse_args: MagicMock) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        with patch("os.makedirs") as mock_make_dirs:
            crypto._make_output_dir("dummy/dir")
            mock_make_dirs.assert_called_once_with("dummy/dir")

    def test_get_link(self, mock_parse_args: MagicMock) -> None:
        crypto: Crypto = Crypto(mock_parse_args)
        with patch.object(crypto, "_get_link_path") as mock_get_link_path:
            crypto._get_link("linkpath")
            mock_get_link_path.assert_called_once_with("linkpath")
