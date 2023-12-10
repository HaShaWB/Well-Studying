import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import 'Scan_format_box.dart';

class home extends StatefulWidget {
  const home({super.key});

  @override
  State<home> createState() => _homeState();
}

class _homeState extends State<home> {
  @override
  Widget build(BuildContext context) {
    // 화면 크기를 계산하여 열 수를 결정합니다.
    double screenWidth = MediaQuery.of(context).size.width;
    int crossAxisCount = (screenWidth / 200).floor(); // 최소 패딩 값을 200으로 설정

    return Scaffold(
      appBar: AppBar(centerTitle: true, title: const Text("문제 스캐너")),
      body: Container(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            children: [
              const Divider(),
              const Text(
                "스캔 기본 포멧을 설정하세요",
                style: TextStyle(color: Colors.black, fontSize: 20),
              ),
              Expanded(
                child: GridView.builder(
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: crossAxisCount, // 박스의 가로 세로 비율
                    crossAxisSpacing: 10, // 가로 방향의 스페이싱
                    mainAxisSpacing: 10, // 세로 방향의 스페이싱
                  ),
                  itemCount: 2,
                  itemBuilder: (BuildContext context, int index) {
                    return const Scan_format_box(
                      title: "수학",
                      sub_title: "평가원 기출",
                    );
                  },
                ),
              ),
              Container(height: 10),
            ],
          ),
        ),
      ),
    );
  }
}
