import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import 'dart:io';
import 'package:path_provider/path_provider.dart';

import '../scan_page/scan_page.dart';

class Scan_format_box extends StatefulWidget {
  final String title;
  final String sub_title;

  const Scan_format_box(
      {Key? key, required this.title, required this.sub_title})
      : super(key: key);

  @override
  _Scan_format_boxState createState() => _Scan_format_boxState();
}

class _Scan_format_boxState extends State<Scan_format_box> {
  bool _isHovering = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (event) => _setHovering(true),
      onExit: (event) => _setHovering(false),
      child: GestureDetector(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => scan_page()),
          );
        },
        child: Container(
          margin: EdgeInsets.all(10),
          decoration: BoxDecoration(
            border: Border.all(color: Colors.black),
            color: _isHovering ? Colors.grey[300] : Colors.white,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Text(
                widget.title,
                style: TextStyle(
                  fontSize: 20,
                ),
              ),
              Text(
                widget.sub_title,
                style: TextStyle(
                  fontSize: 15,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _setHovering(bool isHovering) {
    setState(() {
      _isHovering = isHovering;
    });
  }
}
