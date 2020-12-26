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
    """
    Creates an interactive barplot for use in jupyter notebook.

    Args: df: DataFrame Object
          x: header of the X-axis data
          y: header for the Y-axis data
          title: title of the chart
          color: a color variation representing a third dimension of the chart
          image_path: outputs a .png or .jpg for the plot
          animation_frame: animates the chart given a column header from the df

    -----
    Returns: returns barplot chart,

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

    Args: df: DataFrame Object
          x: header of the X-axis data
          y: header for the Y-axis data
          title: title of the chart
          color: a color variation representing a third dimension of the chart
          image_path: outputs a .png or .jpg for the plot
          animation_frame: animates the chart given a column header from the df

    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
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
    Args: df: DataFrame Object
          x: header of the X-axis data
          y: header for the Y-axis data
          title: title of the chart
          color: a color variation representing a third dimension of the chart
          image_path: outputs a .png or .jpg for the plot
          animation_frame: animates the chart given a column header from the df
    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
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
    Creates an interactive chloropleth chart within jupyter notebook
    Args: df: Dataframe containing charting data
        locations : the location codes. Supports ISO3166 for country coding
          color: Float or integer values of a series in df
          image_path: returns a .jpg or .png if given a path with document name and proper format suffix
          animation_frame:

    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
    """
    fig = px.choropleth(df, locations=locations, color=color,
                        color_continuous_scale="Viridis",
                        animation_frame=animation_frame
                        )
    if image_path:
        fig.write_image(image_path)
    fig.show()


def get_piechart(df, names, values, title=None):
    """
    creates an interactive piechart within a jupyter notebook
    Args: df: DataFrame containing charting data
          names: data representing the names for each fraction of the piechart
          values: data representing the numerical value of each fraction of the piechart
          title : Title of chart
          image_path: returns a .jpg or .png if given a path with document name and proper format suffix

    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
    """
    fig = px.pie(df, values=values, names=names, title=title)
    if image_path:
        fig.write_image(image_path)
    fig.show()
