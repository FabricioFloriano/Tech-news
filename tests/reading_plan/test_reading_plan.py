from unittest.mock import patch
import pytest
from tech_news.analyzer.reading_plan import (
    ReadingPlanService,
)  # noqa: F401, E261, E501


def test_reading_plan_group_news():
    mock = [
        {
            "url": "https://blog.betrybe.com/tecnologia/noticia1",
            "title": "titulo 1",
            "timestamp": "29/11/2023",
            "writer": "Felps",
            "reading_time": 6,
            "summary": "Parágrafo da notícia 1",
            "category": "Tecnologia",
        },
        {
            "url": "https://blog.betrybe.com/tecnologia/noticia2",
            "title": "titulo 2",
            "timestamp": "28/11/2023",
            "writer": "Bux",
            "reading_time": 20,
            "summary": "Parágrafo da notícia 2",
            "category": "Tecnologia",
        },
    ]

    err = "Valor 'available_time' deve ser maior que zero"
    with pytest.raises(ValueError, match=err):
        ReadingPlanService.group_news_for_available_time(-1)

    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        return_value=mock,
    ):
        result = ReadingPlanService.group_news_for_available_time(7)
        assert len(result["readable"]) == 1
        assert len(result["unreadable"]) == 1

        assert result == {
            "readable": [
                {
                    "unfilled_time": 1,
                    "chosen_news": [("titulo 1", 6)],
                }
            ],
            "unreadable": [("titulo 2", 20)],
        }
