from SimLogger import SimLogger
import argparse


def test_save_and_get():
    a = "sample-object"
    simTag = "testing-simTag"
    objTag = "testing-objTag"
    SimLogger.saveObj(simTag, objTag, a)
    aLoadedUniqueId = SimLogger.getObjectFromUniqueId(f"{simTag}_{objTag}")
    aLoadedObjTag = SimLogger.getObj(simTag, objTag)
    assert a == aLoadedUniqueId
    assert a == aLoadedObjTag


def test_save_args():
    # Create a simple argparse parser and parse some test arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--param1", type=int, default=42)
    parser.add_argument("--param2", type=str, default="test_value")
    parser.add_argument("--param3", type=float, default=3.14)

    # Parse with default values
    args = parser.parse_args([])

    simTag = "testing-args-simTag"

    # Save the args
    filePath = SimLogger.saveArgs(simTag, args)

    # Verify the file was created
    assert filePath is not None
    assert "args" in filePath
    assert simTag in filePath

    # Load the args back
    loaded_args = SimLogger.getObj(simTag, "args")

    # Verify the loaded args match the original
    assert loaded_args["param1"] == 42
    assert loaded_args["param2"] == "test_value"
    assert loaded_args["param3"] == 3.14


def test_save_args_with_custom_values():
    # Create a parser and parse with custom values
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=0.001)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--model_name", type=str, default="default")

    # Parse with custom values
    args = parser.parse_args(
        ["--learning_rate", "0.01", "--epochs", "50", "--model_name", "custom_model"]
    )

    simTag = "testing-custom-args"

    # Save the args
    SimLogger.saveArgs(simTag, args, makeNote=True)

    # Load the args back
    loaded_args = SimLogger.getObj(simTag, "args")

    # Verify the loaded args match the custom values
    assert loaded_args["learning_rate"] == 0.01
    assert loaded_args["epochs"] == 50
    assert loaded_args["model_name"] == "custom_model"


def test_argument_parser_auto_save_with_simTag_param():
    # Test automatic saving using ArgumentParser with simTag parameter
    parser = SimLogger.ArgumentParser(simTag="auto-save-test-1")
    parser.add_argument("--param1", type=int, default=100)
    parser.add_argument("--param2", type=str, default="auto_test")

    # Parse args - should automatically save
    parser.parse_args([])

    # Verify the args were automatically saved
    loaded_args = SimLogger.getObj("auto-save-test-1", "args")
    assert loaded_args["param1"] == 100
    assert loaded_args["param2"] == "auto_test"


def test_argument_parser_auto_save_with_setSimTag():
    # Test automatic saving using ArgumentParser with global setSimTag
    SimLogger.setSimTag("auto-save-test-2")
    parser = SimLogger.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=0.002)
    parser.add_argument("--batch_size", type=int, default=64)

    # Parse args - should automatically save using global simTag
    parser.parse_args(["--learning_rate", "0.005", "--batch_size", "128"])

    # Verify the args were automatically saved
    loaded_args = SimLogger.getObj("auto-save-test-2", "args")
    assert loaded_args["learning_rate"] == 0.005
    assert loaded_args["batch_size"] == 128


def test_argument_parser_auto_save_disabled():
    # Test that auto-save can be disabled
    parser = SimLogger.ArgumentParser(simTag="should-not-save", autoSave=False)
    parser.add_argument("--param1", type=int, default=999)

    # Parse args - should NOT automatically save
    parser.parse_args([])

    # Verify the args were NOT saved
    import os

    objFolder = os.path.join("data", "obj")
    fileList = os.listdir(objFolder)
    matching_files = [f for f in fileList if "should-not-save" in f]
    # Should have no files since auto-save was disabled
    assert len(matching_files) == 0
