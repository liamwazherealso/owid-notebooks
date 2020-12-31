import seaborn as sns
import plotly.express as px


def get_barplot(
        df,
        x,
        y,
        title=None,
        color=None,
        animation_frame=None,
        image_path=None):
    """[Summary]

    :param df: DataFrame Object, defaults to [DefaultParamVal]
    :type df: pandas Dataframe Object
    :param x: header of the X-axis data
    :type 
    :param  y: header for the Y-axis data
    :type
    :param title: title of the chart
    :type
    :param color: a color variation representing a third dimension of the chart
    :type
    :param image_path: outputs a .png or .jpg for the plot
    :type
    param animation_frame: animates the chart given a column header from the df
    :type
    :return: returns barplot chart, optional: Exports chart to a given path  .jpg
    :rtype: barplot object, optional: chart as .png or .jpg
    """
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    if image_path:
        fig.write_image(image_path)
    fig.show()


def get_lineplot(
        df,
        x,
        y,
        title=None,
        color=None,
        animation_frame=None,
        image_path=None):
    """
    Creates an interactive lineplot for use in jupyter notebook.

    :param df: DataFrame Object
    :type 
    :param x: header of the X-axis data
    :type:
    :param y: header for the Y-axis data
    :type
    :param title: title of the chart
    :type
    param color: a color variation representing a third dimension of the chart
    :type 
    :param image_path: outputs a .png or .jpg for the plot
    :type
    :param animation_frame: animates the chart given a column header from the df
    :type
    :return: returns barplot chart, optional: Exports chart to a given path  .jpg
    :rtype: barplot object, optional: chart as .png or .jpg
    """

    fig = px.line(df, x=x, y=y, title=title, animation_frame=animation_frame)
    if image_path:
        fig.write_image(image_path)
    fig.show()


def get_scatterplot(
        df,
        x,
        y,
        animation_frame=None,
        title=None,
        color=None,
        image_path=None):
    """
     creates an interactive scatterplot to be used in jupyter notebook
     
    :param df: DataFrame Object[DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    :param x: header of the X-axis data
    :type
    :param y: header for the Y-axis data
    :type
    param title: title of the chart
    type 
    param color: a color variation representing a third dimension of the chart
    :type
    :param image_path: outputs a .png or .jpg for the plot
    :type
    :param animation_frame: animates the chart given a column header from the df
    :type
    :return: returns barplot chart, optional: Exports chart to a given path  .jpg
    :rtype: barplot object, optional: chart as .png or .jpg
    """

    fig = px.scatter(
        df,
        x=x,
        y=y,
        title=title,
        color=color,
        animation_frame=animation_frame)
    if image_path:
        fig.write_image(image_path)
    fig.show()


def get_geoplot(df, locations, color, animation_frame=None, image_path=None):
    """
    creates an interactive chloropleth map in jupyter notebook

    :param df: Dataframe containing charting data
    :type pandas Dataframe object
    :param locations : the location codes. Supports ISO3166 for country coding
    :param color: series containing float and integer values from df
    :type pandas series
    :param image_path: returns a .jpg or .png if given a path I.E. (../charts/chart.jpg)
    :type str
    :param animation_frame:  animates location color based on a given series 
    :type column name of series in df
    :return: returns barplot chart, optional: Export chart as .png or .jpg
    """
    fig = px.choropleth(df, locations=locations, color=color,
                        color_continuous_scale="Viridis",
                        animation_frame=animation_frame
                        )
    if image_path:
        fig.write_image(image_path)
    fig.show()


def get_piechart(df, names, values, title=None,image_path=None):
    """
    creates an interactive piechart within a jupyter notebook
    :param df: DataFrame containing charting data
    :type pandas Dataframe object
    :param names: data representing the names for each fraction of the piechart
    :type series header in df
    :param values: data representing the numerical value of each fraction of the piechart
    :type series header in df
    :param title : Title of chart
    :type str
    :param image_path: returns an image if given a path,optional
    :type .jpg,.png
    :return:returns barplot chart object, optional: Export chart as .png or .jpg
    """
    fig = px.pie(df, values=values, names=names, title=title)
    if image_path:
        fig.write_image(image_path)
    fig.show()
