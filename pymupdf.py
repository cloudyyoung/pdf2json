import fitz
import json


title_color = [1, 0, 0]
subtitle_color = [0, 0, 1]
h3_color = [0, 1, 0]
unknown_text_color = [0.7, 0.7, 0.7]

sizes: set[float] = set()

# assumptions:
# - every time a title appears, a new section begins
#   - we may have to grab the table of contents to validate these, as random text might still have the same font size
# - content text always appears after

# known issues:
# - images have titles, but if we don't include images they might be meaningless
# - text in images isn't useful, but it is being included

omitted_pages = set(
    [
        # 0,
        # 1,
        # 2,
        # 3,
        # 4,
        # 5,
        703,
        704,
    ]
)


humanist777bt_blackb_text = set()

page_number_y_offset = 736.05859375


def add_colored_borders(input_pdf_path, output_pdf_path):  # RGB color for red
    doc = fitz.open(input_pdf_path)

    for index, page in enumerate(doc):
        if index in omitted_pages:
            continue

        blocks = page.get_text("dict")

        for block in blocks["blocks"]:
            for line in block.get("lines") or []:
                for span in line.get("spans") or []:
                    sizes.add(span["size"])
                    rect = fitz.Rect(span["bbox"])

                    if span["text"] == "Reglone Ion Desiccant/Reglone ":
                        print(span)

                    if (
                        span["font"] == "Humanist777BT-BlackB"
                        and span["size"] == 12
                        and span["color"] == 16777215
                        and (
                            # page numbers lose meaning in markdown, so we omit them
                            span["origin"][1] == page_number_y_offset
                            or
                            # left-sided section title (useful for semantics, but not in markdown)
                            span["origin"][0] >= 26.75
                            and span["origin"][0] <= 27
                            or
                            # right-sided section title (useful for semantics, but not in markdown)
                            span["origin"][0] >= 566.5
                            and span["origin"][0] <= 566.8
                        )
                    ):
                        continue

                    elif (
                        (span["size"] == 24 and span["font"] or span["size"] == 26)
                        and span["font"] == "ZurichBT-ExtraBlack"
                    ) or (
                        span["size"] > 21
                        and span["size"] <= 22
                        and span["font"] == "Humanist777BT-BlackB"
                    ):  # title
                        page.draw_rect(
                            rect, color=title_color, fill=None, width=2, overlay=True
                        )
                    elif span["font"] == "Humanist777BT-BlackB" and span["size"] >= 20:
                        print(span)
                    elif span["size"] == 14:  # subtitle
                        page.draw_rect(
                            rect, color=subtitle_color, fill=None, width=2, overlay=True
                        )
                    elif span["size"] == 10 and span["font"] == "ZurichBT-Black":  # h3
                        page.draw_rect(
                            rect, color=h3_color, fill=None, width=2, overlay=True
                        )
                    elif (
                        span["size"] == 8
                        and span["font"] == "ZurichBT-ItalicCondensed"
                        and span["color"] == 2121118
                    ):  # table of contents-like text
                        continue
                    else:
                        page.draw_rect(
                            rect,
                            color=unknown_text_color,
                            fill=None,
                            width=2,
                            overlay=True,
                        )

    print(json.dumps(list(humanist777bt_blackb_text), indent=4))
    doc.save(output_pdf_path)


# Call the function
add_colored_borders(
    # "test/pdf/dc/form/Blue_Book_2023_web.pdf", "test/target/dc/form/bluebook.pdf"
    "test/pdf/dc/form/acuron-label.pdf", "test/target/dc/form/acuron-label.pdf"
)
