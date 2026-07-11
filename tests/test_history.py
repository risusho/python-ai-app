import json

from utils import history


def _use_tmp_history(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"
    monkeypatch.setattr(history, "DATA_DIR", data_dir)
    monkeypatch.setattr(history, "HISTORY_FILE", data_dir / "history.json")


def test_load_history_creates_empty_file_when_missing(monkeypatch, tmp_path):
    _use_tmp_history(monkeypatch, tmp_path)

    result = history.load_history()

    assert result == []
    assert history.HISTORY_FILE.exists()


def test_add_history_prepends_newest_first(monkeypatch, tmp_path):
    _use_tmp_history(monkeypatch, tmp_path)

    history.add_history("ブログ記事作成", "topic-1", "output-1")
    history.add_history("文章要約", "topic-2", "output-2")

    result = history.load_history()

    assert len(result) == 2
    assert result[0]["category"] == "文章要約"
    assert result[0]["input_summary"] == "topic-2"
    assert result[1]["category"] == "ブログ記事作成"
    for item in result:
        assert "timestamp" in item


def test_clear_history_empties_the_file(monkeypatch, tmp_path):
    _use_tmp_history(monkeypatch, tmp_path)

    history.add_history("メール返信作成", "topic", "output")
    history.clear_history()

    assert history.load_history() == []
    assert json.loads(history.HISTORY_FILE.read_text(encoding="utf-8")) == []
