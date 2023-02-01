import unittest


class stackoverflow_question_58692636_test_case(unittest.TestCase):
    def test_stackoverflow_question_58692636(self):
        """
        https://stackoverflow.com/questions/58692636/python-script-fails-to-extract-data-from-xml/58695393#58695393
        """
        from benedict import benedict as bdict

        data_xml = """
        <feed xml:base="http://data.treasury.gov/Feed.svc/">
          <title type="text">DailyTreasuryYieldCurveRateData</title>
          <id>
            http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData
          </id>
          <updated>2019-11-04T07:15:32Z</updated>
          <link rel="self" title="DailyTreasuryYieldCurveRateData" href="DailyTreasuryYieldCurveRateData"/>
          <entry>
            <id>
              http://data.treasury.gov/Feed.svc/DailyTreasuryYieldCurveRateData(7258)
            </id>
            <title type="text"/>
            <updated>2019-11-04T07:15:32Z</updated>
            <author>
              <name/>
            </author>
            <link rel="edit" title="DailyTreasuryYieldCurveRateDatum" href="DailyTreasuryYieldCurveRateData(7258)"/>
            <category term="TreasuryDataWarehouseModel.DailyTreasuryYieldCurveRateDatum" scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme"/>
            <content type="application/xml">
              <m:properties>
                <d:Id m:type="Edm.Int32">7258</d:Id>
                <d:NEW_DATE m:type="Edm.DateTime">2019-01-02T00:00:00</d:NEW_DATE>
                <d:BC_1MONTH m:type="Edm.Double">2.4</d:BC_1MONTH>
                <d:BC_2MONTH m:type="Edm.Double">2.4</d:BC_2MONTH>
                <d:BC_3MONTH m:type="Edm.Double">2.42</d:BC_3MONTH>
                <d:BC_6MONTH m:type="Edm.Double">2.51</d:BC_6MONTH>
                <d:BC_1YEAR m:type="Edm.Double">2.6</d:BC_1YEAR>
                <d:BC_2YEAR m:type="Edm.Double">2.5</d:BC_2YEAR>
                <d:BC_3YEAR m:type="Edm.Double">2.47</d:BC_3YEAR>
                <d:BC_5YEAR m:type="Edm.Double">2.49</d:BC_5YEAR>
                <d:BC_7YEAR m:type="Edm.Double">2.56</d:BC_7YEAR>
                <d:BC_10YEAR m:type="Edm.Double">2.66</d:BC_10YEAR>
                <d:BC_20YEAR m:type="Edm.Double">2.83</d:BC_20YEAR>
                <d:BC_30YEAR m:type="Edm.Double">2.97</d:BC_30YEAR>
                <d:BC_30YEARDISPLAY m:type="Edm.Double">2.97</d:BC_30YEARDISPLAY>
              </m:properties>
            </content>
          </entry>
          <entry>
          <id>
            http://data.treasury.gov/Feed.svc/DailyTreasuryYieldCurveRateData(7259)
          </id>
          <title type="text"/>
          <updated>2019-11-04T07:15:32Z</updated>
          <author>
            <name/>
          </author>
          <link rel="edit" title="DailyTreasuryYieldCurveRateDatum" href="DailyTreasuryYieldCurveRateData(7259)"/>
          <category term="TreasuryDataWarehouseModel.DailyTreasuryYieldCurveRateDatum" scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme"/>
          <content type="application/xml">
            <m:properties>
              <d:Id m:type="Edm.Int32">7259</d:Id>
              <d:NEW_DATE m:type="Edm.DateTime">2019-01-03T00:00:00</d:NEW_DATE>
              <d:BC_1MONTH m:type="Edm.Double">2.42</d:BC_1MONTH>
              <d:BC_2MONTH m:type="Edm.Double">2.42</d:BC_2MONTH>
              <d:BC_3MONTH m:type="Edm.Double">2.41</d:BC_3MONTH>
              <d:BC_6MONTH m:type="Edm.Double">2.47</d:BC_6MONTH>
              <d:BC_1YEAR m:type="Edm.Double">2.5</d:BC_1YEAR>
              <d:BC_2YEAR m:type="Edm.Double">2.39</d:BC_2YEAR>
              <d:BC_3YEAR m:type="Edm.Double">2.35</d:BC_3YEAR>
              <d:BC_5YEAR m:type="Edm.Double">2.37</d:BC_5YEAR>
              <d:BC_7YEAR m:type="Edm.Double">2.44</d:BC_7YEAR>
              <d:BC_10YEAR m:type="Edm.Double">2.56</d:BC_10YEAR>
              <d:BC_20YEAR m:type="Edm.Double">2.75</d:BC_20YEAR>
              <d:BC_30YEAR m:type="Edm.Double">2.92</d:BC_30YEAR>
              <d:BC_30YEARDISPLAY m:type="Edm.Double">2.92</d:BC_30YEARDISPLAY>
            </m:properties>
          </content>
        </entry>
        <entry>
          <id>
            http://data.treasury.gov/Feed.svc/DailyTreasuryYieldCurveRateData(7260)
          </id>
          <title type="text"/>
          <updated>2019-11-04T07:15:32Z</updated>
          <author>
            <name/>
          </author>
          <link rel="edit" title="DailyTreasuryYieldCurveRateDatum" href="DailyTreasuryYieldCurveRateData(7260)"/>
          <category term="TreasuryDataWarehouseModel.DailyTreasuryYieldCurveRateDatum" scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme"/>
          <content type="application/xml">
             <m:properties>
               <d:Id m:type="Edm.Int32">7260</d:Id>
               <d:NEW_DATE m:type="Edm.DateTime">2019-01-04T00:00:00</d:NEW_DATE>
               <d:BC_1MONTH m:type="Edm.Double">2.4</d:BC_1MONTH>
               <d:BC_2MONTH m:type="Edm.Double">2.42</d:BC_2MONTH>
               <d:BC_3MONTH m:type="Edm.Double">2.42</d:BC_3MONTH>
               <d:BC_6MONTH m:type="Edm.Double">2.51</d:BC_6MONTH>
               <d:BC_1YEAR m:type="Edm.Double">2.57</d:BC_1YEAR>
               <d:BC_2YEAR m:type="Edm.Double">2.5</d:BC_2YEAR>
               <d:BC_3YEAR m:type="Edm.Double">2.47</d:BC_3YEAR>
               <d:BC_5YEAR m:type="Edm.Double">2.49</d:BC_5YEAR>
               <d:BC_7YEAR m:type="Edm.Double">2.56</d:BC_7YEAR>
               <d:BC_10YEAR m:type="Edm.Double">2.67</d:BC_10YEAR>
               <d:BC_20YEAR m:type="Edm.Double">2.83</d:BC_20YEAR>
               <d:BC_30YEAR m:type="Edm.Double">2.98</d:BC_30YEAR>
               <d:BC_30YEARDISPLAY m:type="Edm.Double">2.98</d:BC_30YEARDISPLAY>
             </m:properties>
           </content>
         </entry>
        </feed>
        """

        data = bdict.from_xml(data_xml)
        # print(data.dump())
        entries = data["feed.entry"]
        for entry in entries:
            props = bdict(bdict(entry)["content.m:properties"])
            # print(props.dump())
            for key, value in props.items():
                # print(key, value['#text'])
                pass
            # print('-----')
