from core import Settings


def test_default_settings():
    assert hasattr(Settings, "path")
    assert Settings.path == "" or isinstance(Settings.path, str)
    assert Settings.debug is False
    assert Settings.development is False
    assert Settings.verbose is False
    assert Settings.running_module is None
    assert isinstance(Settings.history, list)
    assert isinstance(Settings.previous, list)


def test_settings_history_and_previous():
    Settings.history.clear()
    Settings.previous.clear()
    Settings.running_module = "telegram"
    Settings.update_history("test")
    Settings.update_previous()
    assert Settings.history == ["test"]
    assert Settings.previous == ["telegram"]


def test_module_context_registers_cli_dispatcher():
    from core.Cli import cli

    module_context = cli._load_module_context()
    assert module_context is not None
    assert hasattr(module_context.context, "cli_command_dispatcher")
    assert module_context.context.cli_command_dispatcher is not None


def test_command_use_and_back_sets_module_context():
    from core.Cli import cli

    Settings.running_module = None
    Settings.previous.clear()
    Settings.history.clear()
    Settings.reset_name()

    assert "grabber/telegram" in cli.modules

    cli.command_use("grabber/telegram")
    assert Settings.running_module == "grabber/telegram"
    assert Settings.previous == []
    assert "Module(" in Settings.name

    cli.command_back()
    assert Settings.running_module is False
    assert "Module(" not in Settings.name
