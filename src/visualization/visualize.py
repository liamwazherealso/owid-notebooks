import seaborn as sns
import plotly.express as px

def px_barplot(df,x,y,title=None,color=None,animation_frame=None, image_path=None):
    """
    Args: df
          x
          y
          title
          color
          image_path
          
    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
    
    """
    fig = px.bar(df, x=y, y=y,color=color,title=title)
    if image_path:
        fig.write_image(image_path)
    fig.show()

    
def px_lineplot(df,x,y,title=None,color=None, animation_frame=None,image_path=None):
    """
    Args: df
          x
          y
          title
          color
          image_path
          
    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
    """
    
    fig = px.line(df, x=x, y=y, title=title,animation_frame=animation_frame)
    if image_path:
        fig.write_image(image_path)
    fig.show()

def px_scatterplot(df,x,y,animation_frame=None,title=None,color=None, image_path=None):
    """
    Args: df
          x
          y
          title
          color
          image_path
          
    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
    """

    fig = px.scatter(df,x=x, y=y,title=title,color=color,animation_frame=animation_frame)
    if image_path:
        fig.write_image(image_path)
    fig.show()

def px_geoplot(df,locations,color,animation_frame=None,sliders=None,image_path=None):
    """
    Args: df
          x
          y
          title
          color
          image_path
          sliders
          
    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
    """
    fig=px.choropleth(df, locations=locations, color=color,
                           color_continuous_scale="Viridis",
                           animation_frame=animation_frame
                          )
    if image_path:
        fig.write_image(image_path)
    fig.show()
def px_piechart(df,names,values,title=None):
    """
    Args: df
          x
          y
          title
          color
          image_path
          
    -----
    Returns: returns barplot chart, optional: Export chart as .png or .jpg
    """
    fig = px.pie(df, values=values, names=names, title=title)
    if image_path:
        fig.write_image(image_path)
    fig.show()

def static_lineplot():
    pass
def static_scatterplot():
    pass
def static_barplot():
    pass
def static_geoplot():
    pass
def static_piechart():
    pass
