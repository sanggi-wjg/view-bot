import enum


class BotType(enum.Enum):
    """
    single_visit:
        - 웹 페이지를 한 번 방문하고 종료합니다.
        - web page is visited once and then terminates.

    continuous:
        - 웹 페이지를 지속적으로 방문합니다.
        - web page is visited continuously.

    browsing:
        - 웹 페이지를 탐색하며 여러 페이지를 방문합니다.
        - multiple pages are visited while browsing the web page.
    """

    SINGLE_VISIT = "single_visit"
    CONTINUOUS = "continuous"
    BROWSING = "browsing"
