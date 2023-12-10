import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class Scan_format_box extends StatelessWidget {
  final title;
  final number_of_anchor;
  final anchor_position;

  const Scan_format_box(
      {super.key,
      required String this.title,
      required int this.number_of_anchor,
      required List<int> this.anchor_position});

  @override
  Widget build(BuildContext context) {
    return Container(
        margin: EdgeInsets.all(10),
        decoration: BoxDecoration(
          border: Border.all(color: Colors.black),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Column(
          children: [
            Text(
              title,
              style: TextStyle(
                fontSize: 15,
              ),
            ),
          ],
        ));
  }
}
